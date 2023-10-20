"""simple_wkt: A package to work with simplified WKT objects"""

__version__ = '1.1'

from .geometries import (  # noqa
    WKTObject,
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)
from .parsing import (  # noqa
    parse_wkt,
    parse_point,
    parse_line_string,
    parse_polygon,
    parse_multi_point,
    parse_multi_line_string,
    parse_multi_polygon,
)

__all__ = [
    'WKTObject',
    'PointModel',
    'LineStringModel',
    'PolygonModel',
    'MultiPointModel',
    'MultiLineStringModel',
    'MultiPolygonModel',
    'parse_wkt',
    'parse_point',
    'parse_line_string',
    'parse_polygon',
    'parse_multi_point',
    'parse_multi_line_string',
    'parse_multi_polygon'
]
