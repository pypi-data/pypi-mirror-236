import os
import ee

from .utils import EEType, use_geopandas, get_required_param, get_fields_from_params
from .utils.gee import (
    bands_from_collections,
    get_result, get_result_key, clean_collection, batch_results
)

BATCH_SIZE = int(os.environ.get('EE_BATCH_SIZE_COORDINATES', '30'))


def _data_from_vector(point: ee.Geometry, collection: str, params: dict):
    fields = get_fields_from_params(params)
    collection = ee.FeatureCollection(collection).filterBounds(point)
    return clean_collection(collection, fields)


_DATA_BY_TYPE = {
    EEType.VECTOR.value: _data_from_vector
}


def _run_single_collection(ee_type: str, coords: dict, collection: dict):
    point = ee.Geometry.Point(coords.get('longitude'), coords.get('latitude'))
    return _DATA_BY_TYPE[ee_type](point, collection.get('collection'), collection)


def _run_single(ee_type: str, collections: list, coordinates: list):
    # run each coordinate in sequence, all collections per coordinates
    results = []
    for coords in coordinates:
        for collection in collections:
            result = _run_single_collection(ee_type, coords, collection)
            results.append(get_result(result, get_result_key(collection)))
    return results


def _run_vector(ee_type: str, collections: list, coordinates: list):
    if use_geopandas():
        from .utils.vector import run_by_coordinates
        return run_by_coordinates(collections, coordinates)
    else:
        return _run_single(ee_type, collections, coordinates)


def _batch_processing(bands: ee.Image):
    def process(geometries: list):
        collection = ee.FeatureCollection(geometries)
        return bands.sampleRegions(collection=collection, scale=30)
    return process


def _run_raster(ee_type: str, collections: list, coordinates: list):
    bands = bands_from_collections(collections)
    geometries = [ee.Geometry.Point(coords.get('longitude'), coords.get('latitude')) for coords in coordinates]
    return batch_results(collections, geometries, _batch_processing(bands), batch_size=BATCH_SIZE)


_RUN_BY_TYPE = {
    EEType.VECTOR.value: _run_vector,
    EEType.RASTER.value: _run_raster
}


def run(data: dict):
    ee_type = get_required_param(data, 'ee_type')
    collections = get_required_param(data, 'collections')
    coordinates = get_required_param(data, 'coordinates')
    return _RUN_BY_TYPE[ee_type](ee_type, collections, coordinates)
