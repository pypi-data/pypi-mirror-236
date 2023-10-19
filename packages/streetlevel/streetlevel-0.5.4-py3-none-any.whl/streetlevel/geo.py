import math
from typing import Tuple

import pyproj
from scipy.spatial.transform import Rotation

geod = pyproj.Geod(ellps="WGS84")


def tile_coord_to_wgs84(x: float, y: float, zoom: int) -> Tuple[float, float]:
    """
    Converts XYZ tile coordinates to WGS84 coordinates.

    :param x: X coordinate.
    :param y: Y coordinate.
    :param zoom: Z coordinate.
    :return: WGS84 coordinates.
    """
    scale = 1 << zoom
    lon_deg = x / scale * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / scale)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg
    

def wgs84_to_tile_coord(lat: float, lon: float, zoom: int) -> Tuple[int, int]:
    """
    Converts WGS84 coordinates to XYZ coordinates.

    :param lat: Latitude.
    :param lon: Longitude.
    :param zoom: Z coordinate.
    :return: The X and Y coordinates.
    """
    lat_rad = math.radians(lat)
    scale = 1 << zoom
    x = (lon + 180.0) / 360.0 * scale
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * scale
    return int(x), int(y)


def create_bounding_box_around_point(lat, lon, radius):
    """
    Creates a square bounding box around a point.

    :param lat: Latitude of the center point.
    :param lon: Longitude of the center point.
    :param radius: Shortest distance from the center point to the edges of the square.
    :return: Latitude and longitude of the NW and SE points.
    """
    dist_to_corner = math.sqrt(2 * pow(2 * radius, 2)) / 2
    top_left = geod.fwd(lon, lat, 315, dist_to_corner)
    bottom_right = geod.fwd(lon, lat, 135, dist_to_corner)
    return top_left, bottom_right


def opk_to_rotation(omega: float, phi: float, kappa: float) -> Rotation:
    """
    Creates a SciPy rotation object from omega/phi/kappa angles.
    """
    return Rotation.from_euler('zxy', [phi, -omega, kappa])


def get_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Returns the bearing from point 1 to point 2.

    :param lat1: Latitude of point 1.
    :param lon1: Longitude of point 2.
    :param lat2: Latitude of point 2.
    :param lon2: Longitude of point 2.
    :return: The bearing in radians.
    """
    fwd_azimuth, _, _ = geod.inv(lon1, lat1, lon2, lat2)
    return math.radians(fwd_azimuth)
