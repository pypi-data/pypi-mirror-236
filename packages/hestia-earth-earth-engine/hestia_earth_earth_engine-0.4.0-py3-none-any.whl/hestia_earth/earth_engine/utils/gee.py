import ee
from functools import reduce
from hestia_earth.utils.tools import non_empty_list

from . import get_required_param, get_param

AREA_FIELD = 'areaKm2'
AREA_PERCENT_FIELD = 'areaKm2_percent'
GADM_COLLECTION_PREFIX = 'users/hestiaplatform/gadm36_'


def get_results(response: dict): return list(map(lambda f: f.get('properties'), response.get('features')))


def get_result(response: dict, key: str):
    results = get_results(response)
    result = results[0] if len(results) > 0 else {}
    return result.get(key, result.get('first'))


def get_result_key(collection: dict):
    return (
        collection.get('reducer') or
        collection.get('fields') or
        'mean'
    )


def _date_year(date: str): return int(date.split('-')[0])


def _id_to_level(id: str): return id.count('.')


def load_region(gadm_id: str = '', level: int = None):
    collection = ee.FeatureCollection(f"{GADM_COLLECTION_PREFIX}{level or _id_to_level(gadm_id)}")
    return collection.filterMetadata(
        f"GID_{_id_to_level(gadm_id)}", 'equals', gadm_id.replace('GADM-', '')
    ) if gadm_id else collection


def load_region_geometry(gadm_id: str): return load_region(gadm_id).geometry().getInfo()


def get_point(coordinates: list = None, longitude: float = None, latitude: float = None):
    return ee.Geometry.Point(coordinates) if coordinates else ee.Geometry.Point(longitude, latitude)


def rename_field(before, after):
    def rename_feature(feature):
        return ee.Feature(feature.geometry(), {after: feature.get(before)})
    return rename_feature


def clean_feature(feature: ee.Feature, fields=None, empty_feature=True):
    # will set the geomtry as empty to reduce the volume of the data
    geometry = None if empty_feature else feature.geometry()
    return ee.Feature(geometry).copyProperties(feature, fields if fields is not None and len(fields) > 0 else None)


def clean_collection(collection: ee.FeatureCollection, fields=None, empty_feature=True):
    feature = clean_feature(collection.first(), fields, empty_feature)
    return ee.FeatureCollection([feature]).getInfo()


def area_km2(geometry: ee.Geometry): return geometry.area().divide(1000 * 1000)


def add_area(region: ee.Feature): return region.set({AREA_FIELD: area_km2(region.geometry())})


def add_area_percent(region: ee.Feature, total: float):
    return region.set({AREA_PERCENT_FIELD: ee.Number(region.get(AREA_FIELD)).multiply(100).divide(total)})


def intersect(geometry): return lambda feature: feature.intersection(geometry, 1)


def clip_collection(collection: ee.FeatureCollection, geometry: ee.Geometry): return collection.map(intersect(geometry))


def _aggregate_by_area_first(collection: ee.FeatureCollection, fields: list):
    return clean_collection(collection.sort(AREA_FIELD, False), fields)


def _aggregate_by_area_all(collection: ee.FeatureCollection, fields: list):
    total_area = collection.aggregate_sum(AREA_FIELD).getInfo()
    ffields = fields + [AREA_PERCENT_FIELD]
    return collection.map(lambda f: clean_feature(add_area_percent(f, total_area), ffields)).getInfo()


AGGREGATE_AREA_BY = {
    'first': _aggregate_by_area_first,
    'all': _aggregate_by_area_all
}


def _aggregate_by_area(collection: ee.FeatureCollection, fields=[], reducer='all'):
    return AGGREGATE_AREA_BY[reducer](collection.map(add_area), fields)


def data_from_vector(geometry: ee.Geometry, collection: str, fields: list, reducer: str):
    collection = ee.FeatureCollection(collection).filterBounds(geometry)
    return _aggregate_by_area(clip_collection(collection, geometry), fields, reducer)


GEOMETRY_BY_TYPE = {
    'FeatureCollection': lambda x: _get_geometry_by_type(x.get('features')[0]),
    'GeometryCollection': lambda x: _get_geometry_by_type(x.get('geometries')[0]),
    'Feature': lambda x: x.get('geometry'),
    'Polygon': lambda x: x,
    'MultiPolygon': lambda x: x
}


def _get_geometry_by_type(geojson): return GEOMETRY_BY_TYPE[geojson.get('type')](geojson)


def load_geometry(data: dict): return ee.Geometry(_get_geometry_by_type(data))


def _apply_date_filter(image: ee.Image, year: int):
    return image.filterDate(f"{year}-01-01", f"{year}-12-31").reduce(ee.Reducer.sum())


def _filter_image_by_years(image: ee.Image, start_date: str, end_date: str, reducer_period: str = 'mean'):
    start_year = _date_year(start_date)
    end_year = _date_year(end_date)
    collection = [_apply_date_filter(image, year) for year in range(start_year, end_year + 1)]
    reducer_period_func = getattr(ee.Reducer, reducer_period)
    return ee.ImageCollection(collection).reduce(reducer_period_func())


def _filter_image_by_year(image: ee.Image, year: str):
    return _filter_image_by_years(image, f"{year}-01-01", f"{year}-12-31")


def _image_from_collection(data: dict):
    collection = get_required_param(data, 'collection')
    band_name = get_param(data, 'band_name')
    image = ee.ImageCollection(collection).select(band_name) if band_name else ee.Image(collection)

    year = get_param(data, 'year')
    start_date = get_param(data, 'start_date')
    end_date = get_param(data, 'end_date')
    reducer_period = get_param(data, 'reducer_period', 'mean')

    return _filter_image_by_year(image, year) if year else (
        _filter_image_by_years(image, start_date, end_date, reducer_period) if start_date and end_date
        else image
    )


def bands_from_collections(collections: list):
    images = list(map(_image_from_collection, collections))
    return ee.ImageCollection.fromImages(images).toBands()


def _combine_reducer(reducer, reducer_name: str):
    reducer_func = getattr(ee.Reducer, reducer_name)
    return reducer.combine(reducer2=reducer_func(), sharedInputs=True)


def combine_reducers(values: list):
    reducers = non_empty_list(set([r for r in values if r != 'mean']))
    return reduce(_combine_reducer, reducers, ee.Reducer.mean())


def _order_from_collections(collections: list):
    return [
        '_'.join(non_empty_list([
            str(index),
            c.get('band_name', 'b1'),
            c.get('reducer'),
            f"mean_{c.get('reducer_period', 'mean')}" if any([v in c for v in ['year', 'start_date']]) else None
        ])) for index, c in enumerate(collections)
    ]


def _result_order(result: dict, collections: list):
    band_order = result.get('properties', {}).get('band_order', [])
    columns = [c for c in result.get('columns', {}).keys() if c != 'system:index']
    return band_order if len(band_order) > 0 else (
        columns if len(columns) == 1 else _order_from_collections(collections)
    )


def _reduce_features(order: list):
    def process(values: list, feature: dict):
        properties = feature.get('properties')
        return values + [properties.get(key) for key in order]
    return process


def _process_batch(batch_func, collections: list, geometries: list):
    result = batch_func(geometries).getInfo()
    order = _result_order(result, collections)
    return reduce(_reduce_features(order), result.get('features', []), [])


def batch_results(collections: list, geometries: list, batch_func, batch_size: int):
    batches = range(0, len(geometries), batch_size)
    return reduce(
        lambda prev, curr: prev + _process_batch(batch_func, collections, geometries[curr:curr + batch_size]),
        batches,
        []
    )
