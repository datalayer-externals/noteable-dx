import random
from typing import Optional

import numpy as np
import pandas as pd
import structlog

try:
    import geopandas as gpd
    import shapely.geometry.base
    from shapely.geometry import mapping

    GEOPANDAS_INSTALLED = True
except ImportError:
    GEOPANDAS_INSTALLED = False

logger = structlog.get_logger(__name__)


def generate_latlon_series(num_rows: int):
    """
    Creates a series of shapely.geometry.Point values for latitude and longitude.
    """
    if not GEOPANDAS_INSTALLED:
        logger.warning("geopandas is not installed, skipping generate_latlon_series")
        return np.nan

    lats = [random.randint(-90, 89) + np.random.rand() for _ in range(num_rows)]
    lons = [random.randint(-180, 179) + np.random.rand() for _ in range(num_rows)]
    return gpd.points_from_xy(lons, lats)


def generate_filled_geojson_series(
    num_rows: int,
    existing_latlon_series: Optional[pd.Series] = None,
):
    """
    Creates a series of shapely.geometry.Polygon values by
    generating shapely.geometry.Point values and calling .buffer()
    on them, resulting in circular filled Polygon objects.
    """
    if not GEOPANDAS_INSTALLED:
        logger.warning("geopandas is not installed, skipping filled_geojson_column")
        return np.nan

    if existing_latlon_series is None:
        latlon_series = generate_latlon_series(num_rows)
    else:
        latlon_series = existing_latlon_series
    buffer_series = gpd.GeoSeries(latlon_series).apply(lambda x: x.buffer(np.random.rand()))
    return gpd.GeoSeries(buffer_series)


def generate_exterior_bounds_geojson_series(
    num_rows: int,
    existing_latlon_series: Optional[pd.Series] = None,
):
    """
    Creates a series of shapely.geometry.Polygon values by
    generating shapely.geometry.Point values, calling .buffer()
    on them, and getting the exterior of the resulting object's .envelope,
    resulting in rectangular LineString objects.
    """
    if not GEOPANDAS_INSTALLED:
        logger.warning("geopandas is not installed, skipping exterior_geojson_column")
        return np.nan

    if existing_latlon_series is None:
        latlon_series = generate_latlon_series(num_rows)
    else:
        latlon_series = existing_latlon_series

    envelope_series = gpd.GeoSeries(latlon_series).apply(
        lambda x: x.buffer(np.random.rand()).envelope.exterior
    )
    return gpd.GeoSeries(envelope_series)


def handle_geometry_series(s: pd.Series) -> pd.Series:
    """
    Converts shapely.geometry values to JSON.
    """
    if not GEOPANDAS_INSTALLED:
        return s

    types = (
        shapely.geometry.base.BaseGeometry,
        shapely.geometry.base.BaseMultipartGeometry,
    )
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has geometries; converting to JSON")
        s = s.apply(lambda x: mapping(x) if isinstance(x, types) else x)
    return s