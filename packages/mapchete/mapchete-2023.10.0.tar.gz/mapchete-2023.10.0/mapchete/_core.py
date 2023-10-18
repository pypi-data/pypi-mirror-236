"""Main module managing processes."""

import json
import logging
import multiprocessing
import os
import threading
import warnings

from cachetools import LRUCache

from mapchete._processing import (
    ProcessInfo,
    _preprocess,
    _run_area,
    _run_on_single_tile,
    compute,
    task_batches,
)
from mapchete._tasks import TileTask
from mapchete._timer import Timer
from mapchete.config import MULTIPROCESSING_DEFAULT_START_METHOD, MapcheteConfig
from mapchete.errors import MapcheteNodataTile, ReprojectionFailed
from mapchete.formats import read_output_metadata
from mapchete.io import MPath, fs_from_path, tiles_exist
from mapchete.stac import tile_direcotry_item_to_dict, update_tile_directory_stac_item
from mapchete.tile import count_tiles
from mapchete.validate import validate_tile, validate_zooms

logger = logging.getLogger(__name__)


def open(some_input, with_cache=False, fs=None, fs_kwargs=None, **kwargs):
    """
    Open a Mapchete process.

    Parameters
    ----------
    some_input : MapcheteConfig object, config dict, path to mapchete file or path to
        TileDirectory
        Mapchete process configuration
    mode : string
        * ``memory``: Generate process output on demand without reading
          pre-existing data or writing new data.
        * ``readonly``: Just read data without processing new data.
        * ``continue``: (default) Don't overwrite existing output.
        * ``overwrite``: Overwrite existing output.
    zoom : list or integer
        process zoom level or a pair of minimum and maximum zoom level
    bounds : tuple
        left, bottom, right, top process boundaries in output pyramid
    single_input_file : string
        single input file if supported by process
    with_cache : bool
        process output data cached in memory
    fs : fsspec FileSystem
        Any FileSystem object for the mapchete output.
    fs_kwargs : dict
        Special configuration parameters if FileSystem object has to be created.

    Returns
    -------
    Mapchete
        a Mapchete process object
    """
    # convert to MPath object if possible
    if isinstance(some_input, str):
        some_input = MPath.from_inp(some_input)
    # for TileDirectory inputs
    if isinstance(some_input, MPath) and some_input.suffix == "":
        logger.debug("assuming TileDirectory")
        metadata_json = MPath.from_inp(some_input).joinpath("metadata.json")
        fs_kwargs = fs_kwargs or {}
        fs = fs or fs_from_path(metadata_json, **fs_kwargs)
        logger.debug("read metadata.json")
        metadata = read_output_metadata(metadata_json, fs=fs)
        config = dict(
            process=None,
            input=None,
            pyramid=metadata["pyramid"].to_dict(),
            output=dict(
                {
                    k: v
                    for k, v in metadata["driver"].items()
                    if k not in ["delimiters", "mode"]
                },
                path=some_input,
                fs=fs,
                fs_kwargs=fs_kwargs,
                **kwargs,
            ),
            config_dir=os.getcwd(),
            zoom_levels=kwargs.get("zoom"),
        )
        kwargs.update(mode="readonly")
        return Mapchete(MapcheteConfig(config, **kwargs))
    # for dicts, .mapchete file paths or MpacheteConfig objects
    elif (
        isinstance(some_input, dict)
        or isinstance(some_input, MPath)
        and some_input.suffix == ".mapchete"
        or isinstance(some_input, MapcheteConfig)
    ):
        return Mapchete(MapcheteConfig(some_input, **kwargs), with_cache=with_cache)
    else:  # pragma: no cover
        raise TypeError(
            "can only open input in form of a mapchete file path, a TileDirectory path, "
            f"a dictionary or a MapcheteConfig object, not {type(some_input)}"
        )


class Mapchete(object):
    """
    Main entry point to every processing job.

    From here, the process tiles can be determined and executed.

    Parameters
    ----------
    config : MapcheteConfig
        Mapchete process configuration
    with_cache : bool
        cache processed output data in memory (default: False)

    Attributes
    ----------
    config : MapcheteConfig
        Mapchete process configuration
    with_cache : bool
        process output data cached in memory
    """

    def __init__(self, config, with_cache=False):
        """
        Initialize Mapchete processing endpoint.

        Parameters
        ----------
        config : MapcheteConfig
            Mapchete process configuration
        with_cache : bool
            cache processed output data in memory (default: False)
        """
        logger.info("initialize process")
        if not isinstance(config, MapcheteConfig):
            raise TypeError("config must be MapcheteConfig object")
        self.config = config
        self.with_cache = True if self.config.mode == "memory" else with_cache
        if self.with_cache:
            self.process_tile_cache = LRUCache(maxsize=512)
            self.current_processes = {}
            self.process_lock = threading.Lock()
        self._count_tiles_cache = {}

    def get_process_tiles(self, zoom=None, batch_by=None):
        """
        Yield process tiles.

        Tiles intersecting with the input data bounding boxes as well as
        process bounds, if provided, are considered process tiles. This is to
        avoid iterating through empty tiles.

        Parameters
        ----------
        zoom : integer
            zoom level process tiles should be returned from; if none is given,
            return all process tiles
        batch_by : str
            if not None, tiles can be yielded in batches either by "row" or "column".

        yields
        ------
        BufferedTile objects
        """
        logger.debug("get process tiles...")
        if zoom or zoom == 0:
            for tile in self.config.process_pyramid.tiles_from_geom(
                self.config.area_at_zoom(zoom),
                zoom=zoom,
                batch_by=batch_by,
                exact=True,
            ):
                yield tile
        else:
            for i in self.config.zoom_levels.descending():
                for tile in self.config.process_pyramid.tiles_from_geom(
                    self.config.area_at_zoom(i), zoom=i, batch_by=batch_by, exact=True
                ):
                    yield tile

    def skip_tiles(self, tiles=None, tiles_batches=None):
        """
        Quickly determine whether tiles can be skipped for processing.

        The skip value is True if process mode is 'continue' and process output already
        exists. In all other cases, skip is False.

        Parameters
        ----------
        tiles : list of process tiles

        Yields
        ------
        tuples : (tile, skip)
        """
        logger.debug("determine which tiles to skip...")
        # only check for existing output in "continue" mode
        if self.config.mode == "continue":
            yield from tiles_exist(
                config=self.config,
                process_tiles=tiles,
                process_tiles_batches=tiles_batches,
            )
        # otherwise don't skip tiles
        else:
            if tiles_batches:
                for batch in tiles_batches:
                    for tile in batch:
                        yield (tile, False)
            else:
                for tile in tiles:
                    yield (tile, False)

    def task_batches(self, zoom=None, tile=None, skip_output_check=False, **kwargs):
        """
        Generate task batches from preprocessing tasks and tile tasks.
        """
        yield from task_batches(
            self, zoom=zoom, tile=tile, skip_output_check=skip_output_check, **kwargs
        )

    def compute(self, **kwargs):
        """Compute preprocessing tasks and tile tasks in one go."""
        yield from compute(self, **kwargs)

    def batch_preprocessor(
        self,
        dask_scheduler=None,
        dask_max_submitted_tasks=500,
        dask_chunksize=100,
        workers=None,
        executor=None,
    ):
        """
        Run all required preprocessing steps and yield over results.

        The task count can be determined by self.config.preprocessing_tasks_count().

        Parameters
        ----------

        dask_schedulter : str
            URL to a dask scheduler if distributed execution is desired
        dask_max_submitted_tasks : int
            Make sure that not more tasks are submitted to dask scheduler at once. (default: 500)
        dask_chunksize : int
            Number of tasks submitted to the scheduler at once. (default: 100)
        workers : int
            number of workers to be used for local processing
        executor : mapchete.Executor
            optional executor class to be used for processing

        """
        # process everything using executor and yield from results
        yield from _preprocess(
            self.config.preprocessing_tasks(),
            process=self,
            dask_scheduler=dask_scheduler,
            dask_max_submitted_tasks=dask_max_submitted_tasks,
            dask_chunksize=dask_chunksize,
            workers=workers,
            executor=executor,
        )

    def batch_preprocess(
        self,
        dask_scheduler=None,
        dask_max_submitted_tasks=500,
        dask_chunksize=100,
        workers=None,
        executor=None,
    ):
        """
        Run all required preprocessing steps.

        Parameters
        ----------

        dask_schedulter : str
            URL to a dask scheduler if distributed execution is desired
        dask_max_submitted_tasks : int
            Make sure that not more tasks are submitted to dask scheduler at once. (default: 500)
        dask_chunksize : int
            Number of tasks submitted to the scheduler at once. (default: 100)
        workers : int
            number of workers to be used for local processing
        executor : mapchete.Executor
            optional executor class to be used for processing
        """
        list(
            self.batch_preprocessor(
                dask_scheduler=dask_scheduler,
                dask_max_submitted_tasks=dask_max_submitted_tasks,
                dask_chunksize=dask_chunksize,
                workers=workers,
                executor=executor,
            )
        )

    def batch_process(
        self,
        zoom=None,
        tile=None,
        dask_scheduler=None,
        dask_max_submitted_tasks=500,
        dask_chunksize=100,
        multi=None,
        workers=None,
        multiprocessing_module=None,
        multiprocessing_start_method=MULTIPROCESSING_DEFAULT_START_METHOD,
        skip_output_check=False,
        executor=None,
    ):
        """
        Process a large batch of tiles.

        Parameters
        ----------
        process : MapcheteProcess
            process to be run
        zoom : list or int
            either single zoom level or list of minimum and maximum zoom level;
            None processes all (default: None)
        tile : tuple
            zoom, row and column of tile to be processed (cannot be used with
            zoom)
        workers : int
            number of workers (default: number of CPU cores)
        dask_schedulter : str
            URL to a dask scheduler if distributed execution is desired
        dask_max_submitted_tasks : int
            Make sure that not more tasks are submitted to dask scheduler at once. (default: 500)
        dask_chunksize : int
            Number of tasks submitted to the scheduler at once. (default: 100)
        multiprocessing_module : module
            either Python's standard 'multiprocessing' or Celery's 'billiard' module
            (default: multiprocessing)
        multiprocessing_start_method : str
            "fork", "forkserver" or "spawn"
            (default: "spawn")
        skip_output_check : bool
            skip checking whether process tiles already have existing output before
            starting to process;
        executor : mapchete.Executor
            optional executor class to be used for processing
        """
        list(
            self.batch_processor(
                zoom=zoom,
                tile=tile,
                dask_scheduler=dask_scheduler,
                dask_max_submitted_tasks=dask_max_submitted_tasks,
                dask_chunksize=dask_chunksize,
                workers=workers,
                multi=multi,
                multiprocessing_module=multiprocessing_module,
                multiprocessing_start_method=multiprocessing_start_method,
                skip_output_check=skip_output_check,
                executor=executor,
            )
        )

    def batch_processor(
        self,
        zoom=None,
        tile=None,
        dask_scheduler=None,
        dask_max_submitted_tasks=500,
        dask_chunksize=100,
        multi=None,
        workers=None,
        multiprocessing_module=None,
        multiprocessing_start_method=MULTIPROCESSING_DEFAULT_START_METHOD,
        skip_output_check=False,
        executor=None,
    ):
        """
        Process a large batch of tiles and yield report messages per tile.

        Parameters
        ----------
        zoom : list or int
            either single zoom level or list of minimum and maximum zoom level;
            None processes all (default: None)
        tile : tuple
            zoom, row and column of tile to be processed (cannot be used with
            zoom)
        dask_schedulter : str
            URL to a dask scheduler if distributed execution is desired
        dask_max_submitted_tasks : int
            Make sure that not more tasks are submitted to dask scheduler at once. (default: 500)
        dask_chunksize : int
            Number of tasks submitted to the scheduler at once. (default: 100)
        multi : int
            number of workers (default: number of CPU cores)
        multiprocessing_module : module
            either Python's standard 'multiprocessing' or Celery's 'billiard' module
            (default: multiprocessing)
        multiprocessing_start_method : str
            "fork", "forkserver" or "spawn"
            (default: "spawn")
        skip_output_check : bool
            skip checking whether process tiles already have existing output before
            starting to process;
        executor : mapchete.Executor
            optional executor class to be used for processing
        """
        if multi is not None:  # pragma: no cover
            warnings.warn(
                DeprecationWarning(
                    "the 'multi' keyword is deprecated and should be called 'workers'"
                )
            )
            workers = workers or multi

        if zoom and tile:
            raise ValueError("use either zoom or tile")

        # run single tile
        if tile:
            yield _run_on_single_tile(
                executor=executor,
                dask_scheduler=dask_scheduler,
                process=self,
                tile=self.config.process_pyramid.tile(*tuple(tile)),
            ).result()
        # run area
        else:
            for future in _run_area(
                process=self,
                zoom_levels=_get_zoom_level(zoom, self),
                dask_scheduler=dask_scheduler,
                dask_max_submitted_tasks=dask_max_submitted_tasks,
                dask_chunksize=dask_chunksize,
                workers=workers or multiprocessing.cpu_count(),
                multiprocessing_module=multiprocessing_module or multiprocessing,
                multiprocessing_start_method=multiprocessing_start_method,
                skip_output_check=skip_output_check,
                executor=executor,
            ):
                yield future.result()

    def count_tasks(self, minzoom=None, maxzoom=None, init_zoom=0):
        """
        Count all preprocessing tasks and tiles at given zoom levels.

        Parameters
        ----------
        minzoom : int
            limits minimum process zoom
        maxzoom : int
            limits maximum process zoom
        init_zoom : int
            initial zoom level used for tile count algorithm

        Returns
        -------
        number of tasks
        """
        return self.config.preprocessing_tasks_count() + self.count_tiles(
            minzoom=minzoom, maxzoom=maxzoom, init_zoom=0
        )

    def count_tiles(self, minzoom=None, maxzoom=None, init_zoom=0):
        """
        Count number of tiles intersecting with process area at given zoom levels.

        Parameters
        ----------
        minzoom : int
            limits minimum process zoom
        maxzoom : int
            limits maximum process zoom
        init_zoom : int
            initial zoom level used for tile count algorithm

        Returns
        -------
        number of tiles
        """
        minzoom = self.config.init_zoom_levels.min if minzoom is None else minzoom
        maxzoom = self.config.init_zoom_levels.max if maxzoom is None else maxzoom
        if (minzoom, maxzoom) not in self._count_tiles_cache:
            logger.debug("counting tiles...")
            with Timer() as t:
                self._count_tiles_cache[(minzoom, maxzoom)] = count_tiles(
                    self.config.area_at_zoom(),
                    self.config.process_pyramid,
                    minzoom,
                    maxzoom,
                    init_zoom=init_zoom,
                )
            logger.debug("tiles counted in %s", t)
        return self._count_tiles_cache[(minzoom, maxzoom)]

    def execute(self, process_tile, raise_nodata=False):
        """
        Run Mapchete process on a tile.

        Execute, write and return data.

        Parameters
        ----------
        process_tile : Tile or tile index tuple
            Member of the process tile pyramid (not necessarily the output
            pyramid, if output has a different metatiling setting)

        Returns
        -------
        data : NumPy array or features
            process output
        """
        process_tile = validate_tile(process_tile, self.config.process_pyramid)
        self.batch_preprocess()
        try:
            return self.config.output.streamline_output(
                TileTask(tile=process_tile, config=self.config).execute()
            )
        except MapcheteNodataTile:
            if raise_nodata:  # pragma: no cover
                raise
            return self.config.output.empty(process_tile)

    def read(self, output_tile):
        """
        Read from written process output.

        Parameters
        ----------
        output_tile : BufferedTile or tile index tuple
            Member of the output tile pyramid (not necessarily the process
            pyramid, if output has a different metatiling setting)

        Returns
        -------
        data : NumPy array or features
            process output
        """
        output_tile = validate_tile(output_tile, self.config.output_pyramid)
        if self.config.mode not in ["readonly", "continue", "overwrite"]:
            raise ValueError("process mode must be readonly, continue or overwrite")
        return self.config.output.read(output_tile)

    def write(self, process_tile, data):
        """
        Write data into output format.

        Parameters
        ----------
        process_tile : BufferedTile or tile index tuple
            process tile
        data : NumPy array or features
            data to be written
        """
        process_tile = validate_tile(process_tile, self.config.process_pyramid)
        if self.config.mode not in ["continue", "overwrite"]:
            raise ValueError("cannot write output in current process mode")

        if self.config.mode == "continue" and (
            self.config.output.tiles_exist(process_tile)
        ):
            message = "output exists, not overwritten"
            logger.debug((process_tile.id, message))
            return ProcessInfo(
                tile=process_tile,
                processed=False,
                process_msg=None,
                written=False,
                write_msg=message,
            )
        elif data is None:
            message = "output empty, nothing written"
            logger.debug((process_tile.id, message))
            return ProcessInfo(
                tile=process_tile,
                processed=False,
                process_msg=None,
                written=False,
                write_msg=message,
            )
        else:
            with Timer() as t:
                self.config.output.write(process_tile=process_tile, data=data)
            message = "output written in %s" % t
            logger.debug((process_tile.id, message))
            return ProcessInfo(
                tile=process_tile,
                processed=False,
                process_msg=None,
                written=True,
                write_msg=message,
            )

    def get_raw_output(self, tile, _baselevel_readonly=False):
        """
        Get output raw data.

        This function won't work with multiprocessing, as it uses the
        ``threading.Lock()`` class.

        Parameters
        ----------
        tile : tuple, Tile or BufferedTile
            If a tile index is given, a tile from the output pyramid will be
            assumed. Tile cannot be bigger than process tile!

        Returns
        -------
        data : NumPy array or features
            process output
        """
        tile = validate_tile(tile, self.config.output_pyramid)
        tile = (
            self.config.baselevels["tile_pyramid"].tile(*tile.id)
            if _baselevel_readonly
            else tile
        )

        # Return empty data if zoom level is outside of process zoom levels.
        if tile.zoom not in self.config.zoom_levels:
            return self.config.output.empty(tile)

        # TODO implement reprojection
        if tile.crs != self.config.process_pyramid.crs:
            raise NotImplementedError(
                "reprojection between processes not yet implemented"
            )

        if self.config.mode == "memory":
            # Determine affected process Tile and check whether it is already
            # cached.
            process_tile = self.config.process_pyramid.intersecting(tile)[0]
            return self._extract(
                in_tile=process_tile,
                in_data=self._execute_using_cache(process_tile),
                out_tile=tile,
            )

        # TODO: cases where tile intersects with multiple process tiles
        process_tile = self.config.process_pyramid.intersecting(tile)[0]

        # get output_tiles that intersect with current tile
        if tile.pixelbuffer > self.config.output.pixelbuffer:
            output_tiles = list(
                self.config.output_pyramid.tiles_from_bounds(tile.bounds, tile.zoom)
            )
        else:
            output_tiles = self.config.output_pyramid.intersecting(tile)

        if self.config.mode == "readonly" or _baselevel_readonly:
            if self.config.output.tiles_exist(process_tile):
                return self._read_existing_output(tile, output_tiles)
            else:
                return self.config.output.empty(tile)
        elif self.config.mode == "continue" and not _baselevel_readonly:
            if self.config.output.tiles_exist(process_tile):
                return self._read_existing_output(tile, output_tiles)
            else:
                return self._process_and_overwrite_output(tile, process_tile)
        elif self.config.mode == "overwrite" and not _baselevel_readonly:
            return self._process_and_overwrite_output(tile, process_tile)

    def write_stac(self, indent=4):
        """
        Create or update existing STAC JSON file.

        On TileDirectory outputs, the tiled-assets are updated regarding
        zoom levels and bounds.
        """
        try:
            import pystac
        except ImportError:  # pragma: no cover
            logger.warning("install extra mapchete[stac] to write STAC item files")
            return

        if not self.config.output.use_stac or self.config.mode in [
            "readonly",
            "memory",
        ]:
            return
        # read existing STAC file
        try:
            with self.config.output.stac_path.open("r") as src:
                item = pystac.read_dict(json.loads(src.read()))
        except FileNotFoundError:
            item = None
        try:
            item = update_tile_directory_stac_item(
                item=item,
                item_path=str(self.config.output.stac_path),
                item_id=self.config.output.stac_item_id,
                zoom_levels=self.config.init_zoom_levels,
                bounds=self.config.effective_bounds,
                item_metadata=self.config.output.stac_item_metadata,
                tile_pyramid=self.config.output_pyramid,
                bands_type=self.config.output.stac_asset_type,
                band_asset_template=self.config.output.tile_path_schema,
            )
            logger.debug("write STAC item JSON to %s", self.config.output.stac_path)
            self.config.output.stac_path.parent.makedirs()
            with self.config.output.stac_path.open("w") as dst:
                dst.write(json.dumps(tile_direcotry_item_to_dict(item), indent=indent))
        except ReprojectionFailed:
            logger.warning(
                "cannot create STAC item because footprint cannot be reprojected into EPSG:4326"
            )
        except Exception as exc:  # pragma: no cover
            logger.warning("cannot create or update STAC item: %s", str(exc))

    def _process_and_overwrite_output(self, tile, process_tile):
        if self.with_cache:
            output = self._execute_using_cache(process_tile)
        else:
            output = self.execute(process_tile)

        self.write(process_tile, output)
        return self._extract(in_tile=process_tile, in_data=output, out_tile=tile)

    def _read_existing_output(self, tile, output_tiles):
        return self.config.output.extract_subset(
            input_data_tiles=[
                (output_tile, self.read(output_tile)) for output_tile in output_tiles
            ],
            out_tile=tile,
        )

    def _execute_using_cache(self, process_tile):
        # Extract Tile subset from process Tile and return.
        try:
            return self.process_tile_cache[process_tile.id]
        except KeyError:
            # Lock process for Tile or wait.
            with self.process_lock:
                process_event = self.current_processes.get(process_tile.id)
                if not process_event:
                    self.current_processes[process_tile.id] = threading.Event()
            # Wait and return.
            if process_event:  # pragma: no cover
                process_event.wait()
                return self.process_tile_cache[process_tile.id]
            else:
                try:
                    output = self.execute(process_tile)
                    self.process_tile_cache[process_tile.id] = output
                    if self.config.mode in ["continue", "overwrite"]:
                        self.write(process_tile, output)
                    return self.process_tile_cache[process_tile.id]
                finally:
                    with self.process_lock:
                        process_event = self.current_processes.get(process_tile.id)
                        del self.current_processes[process_tile.id]
                        process_event.set()

    def _extract(self, in_tile=None, in_data=None, out_tile=None):
        """Extract data from tile."""
        return self.config.output.extract_subset(
            input_data_tiles=[(in_tile, in_data)], out_tile=out_tile
        )

    def __enter__(self):
        """Enable context manager."""
        return self

    def __exit__(self, exc_type=None, exc_value=None, exc_traceback=None):
        """Cleanup on close."""
        # write/update STAC metadata
        if exc_type is None:
            self.write_stac()
        # run input drivers cleanup
        for ip in self.config.input.values():
            if ip is not None:
                logger.debug(f"running cleanup on {ip}...")
                ip.cleanup()
        # run output driver cleanup
        logger.debug(f"closing output driver {self.config.output}...")
        # HINT: probably cleaner to use the outputs __exit__ function and use a contextmanager interface
        self.config.output.close(
            exc_type=exc_type, exc_value=exc_value, exc_traceback=exc_traceback
        )
        # clean up internal cache
        if self.with_cache:
            self.process_tile_cache = None
            self.current_processes = None
            self.process_lock = None

    def __repr__(self):  # pragma: no cover
        return f"Mapchete <process_name={self.config.process.name}>"


def _get_zoom_level(zoom, process):
    """Determine zoom levels."""
    return process.config.zoom_levels if zoom is None else validate_zooms(zoom)
