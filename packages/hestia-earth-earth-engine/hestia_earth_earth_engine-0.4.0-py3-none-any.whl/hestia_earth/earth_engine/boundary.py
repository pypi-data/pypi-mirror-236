import os
import ee

from .utils import EEType, use_geopandas, get_param, get_required_param, get_fields_from_params
from .utils.gee import (
    load_geometry, area_km2,
    bands_from_collections,
    get_result, get_result_key, data_from_vector,
    batch_results, combine_reducers
)

BATCH_SIZE = int(os.environ.get('EE_BATCH_SIZE_BOUNDARY', '5000'))


def get_size_km2(boundary: dict):
    return area_km2(load_geometry(boundary)).getInfo()


def _data_from_vector(geometry: ee.Geometry, collection: str, params: dict):
    fields = get_fields_from_params(params)
    reducer = get_param(params, 'reducer', 'first')
    return data_from_vector(geometry, collection, fields, reducer)


_DATA_BY_TYPE = {
    EEType.VECTOR.value: _data_from_vector
}


def _run_single_collection(ee_type: str, geometry: ee.Geometry, collection: dict):
    return _DATA_BY_TYPE[ee_type](geometry, collection.get('collection'), collection)


def _run_single(ee_type: str, collections: list, boundaries: list):
    # run each coordinate in sequence, all collections per boundaries
    results = []
    for boundary in boundaries:
        geometry = load_geometry(boundary)
        for collection in collections:
            result = _run_single_collection(ee_type, geometry, collection)
            results.append(get_result(result, get_result_key(collection)))
    return results


def _run_vector(ee_type: str, collections: list, boundaries: list):
    if use_geopandas():
        from .utils.vector import run_by_boundaries
        return run_by_boundaries(collections, boundaries)
    else:
        return _run_single(ee_type, collections, boundaries)


def _batch_processing(bands: ee.Image, reducers: list):
    def process(geometries: list):
        collection = ee.FeatureCollection(geometries)
        return bands.reduceRegions(**{
            'reducer': reducers,
            'collection': collection,
            'scale': 30,
        })
    return process


def _run_raster(ee_type: str, collections: list, boundaries: list):
    bands = bands_from_collections(collections)
    reducers = [v.get('reducer') for v in collections]
    combined_reducers = combine_reducers(reducers)
    geometries = list(map(load_geometry, boundaries))
    return batch_results(collections, geometries, _batch_processing(bands, combined_reducers), batch_size=BATCH_SIZE)


_RUN_BY_TYPE = {
    EEType.VECTOR.value: _run_vector,
    EEType.RASTER.value: _run_raster
}


def run(data: dict):
    ee_type = get_required_param(data, 'ee_type')
    collections = get_required_param(data, 'collections')
    boundaries = get_required_param(data, 'boundaries')
    return _RUN_BY_TYPE[ee_type](ee_type, collections, boundaries)
