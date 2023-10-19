import os
import ee

from .utils import EEType, use_geopandas, get_param, get_required_param, get_fields_from_params
from .utils.gee import (
    load_region, area_km2, get_point,
    bands_from_collections,
    get_result, get_result_key, data_from_vector,
    batch_results, combine_reducers
)

BATCH_SIZE = int(os.environ.get('EE_BATCH_SIZE_GADM', '5000'))

DEFAULT_SCALE = 30
DEFAULT_YEAR = 2000


def get_size_km2(gadm_id: str):
    region = load_region(gadm_id)
    return area_km2(region.geometry()).getInfo()


def get_distance_to_coordinates(gadm_id: str, latitude: float, longitude: float):
    """
    Returns the distance between the coordinates and the GADM region, in meters.
    """
    region = load_region(gadm_id)
    coordinates = get_point(longitude=longitude, latitude=latitude)
    return region.geometry().distance(coordinates).getInfo()


def get_id_by_coordinates(level: int, latitude: float, longitude: float):
    """
    Returns the GADM ID of the closest region to the coordinates by level (0 to 5).
    """
    collection = load_region(level=level)
    coordinates = get_point(longitude=longitude, latitude=latitude)
    region = collection.filterBounds(coordinates).first()
    return region.get(f"GID_{level}").getInfo()


def _data_from_vector(region: ee.FeatureCollection, collection: str, params: dict):
    fields = get_fields_from_params(params)
    reducer = get_param(params, 'reducer', 'first')
    return data_from_vector(region.geometry(), collection, fields, reducer)


_DATA_BY_TYPE = {
    EEType.VECTOR.value: _data_from_vector
}


def _run_single_collection(ee_type: str, geometry: ee.FeatureCollection, collection: dict):
    return _DATA_BY_TYPE[ee_type](geometry, collection.get('collection'), collection)


def _run_single(ee_type: str, collections: list, gadm_ids: list):
    # run each coordinate in sequence, all collections per gadm ID
    results = []
    for gadm_id in gadm_ids:
        region = load_region(gadm_id)
        for collection in collections:
            result = _run_single_collection(ee_type, region, collection)
            results.append(get_result(result, get_result_key(collection)))
    return results


def _run_vector(ee_type: str, collections: list, gadm_ids: list):
    if use_geopandas():
        from .utils.vector import run_by_gadm_ids
        return run_by_gadm_ids(collections, gadm_ids)
    else:
        return _run_single(ee_type, collections, gadm_ids)


def _batch_processing(bands: ee.Image, reducers: list):
    def process(geometries: list):
        collection = ee.FeatureCollection(geometries)
        return bands.reduceRegions(**{
            'reducer': reducers,
            'collection': collection,
            'scale': 30,
        })
    return process


def _run_raster(ee_type: str, collections: list, gadm_ids: list):
    bands = bands_from_collections(collections)
    reducers = combine_reducers(collections)
    geometries = [load_region(g).geometry() for g in gadm_ids]
    return batch_results(collections, geometries, _batch_processing(bands, reducers), batch_size=BATCH_SIZE)


_RUN_BY_TYPE = {
    EEType.VECTOR.value: _run_vector,
    EEType.RASTER.value: _run_raster
}


def run(data: dict):
    ee_type = get_required_param(data, 'ee_type')
    collections = get_required_param(data, 'collections')
    gadm_ids = get_required_param(data, 'gadm-ids')
    return _RUN_BY_TYPE[ee_type](ee_type, collections, gadm_ids)
