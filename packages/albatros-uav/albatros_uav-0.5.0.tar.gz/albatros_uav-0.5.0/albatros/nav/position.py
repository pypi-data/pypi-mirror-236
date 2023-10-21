"""Module containing functions related to position processing."""

import math
from dataclasses import dataclass
from typing import Type, TypeVar

_T = TypeVar("_T")


@dataclass
class PositionNED:
    """
    :param north: meters from reference point in north direction
    :param north: meters from reference point in east direction
    :param north: meters from reference point in down
    """

    north: float = 0
    east: float = 0
    down: float = 0


@dataclass
class PositionGPS:
    """
    :param lat: Latitude (degE7)
    :param lon: Longitude (degE7)
    :param alt: Altitude (m)
    """

    lat: int = 0
    lon: int = 0
    alt: float = 0

    def get_global_position_float(self) -> tuple[float, float, float]:
        return (self.lat / 1.0e7, self.lon / 1.0e7, self.alt)

    def scale_global_position(self, lat: float, lon: float, alt: float) -> None:
        self.lat = int(lat * 1.0e7)
        self.lon = int(lon * 1.0e7)
        self.alt = alt

    @classmethod
    def from_float_position(cls: Type[_T], lat: float, lon: float, alt: float) -> _T:
        """Create ``PositionGPS`` object from float coordinates.

        :param lat: Latitude (deg)
        :param lon: Longitude (deg)
        :param alt: Altitude (m)
        """
        lat_int = int(lat * 1.0e7)
        lon_int = int(lon * 1.0e7)
        return cls(lat_int, lon_int, alt)  # type: ignore


def ned2geo(reference_point: PositionGPS, point: PositionNED) -> PositionGPS:
    """
    Converts GEO to NED coordinates.

    :param reference_point: reference point (origin of the coordinate system)
    :param point: NED point to be converted to GEO
    :reurn: GEO coordinate of point
    """
    lat_float, lon_float, alt = reference_point.get_global_position_float()

    lat = (point.north / (40075704.0 / 360)) + lat_float
    lon = (
        point.east / (math.cos(math.radians(lat_float)) * (40075704.0 / 360))
    ) + lon_float
    return PositionGPS.from_float_position(lat, lon, point.down)


def distance_between_points(point1: PositionGPS, point2: PositionGPS) -> float:
    """Calculate the distance between two GPS points using the Haversine formula.

    :param point1: The first GPS position.
    :param point2: The second GPS position.

    :return: The distance between the two points in meters.
    """
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(point1.lat / 1.0e7)
    lon1 = math.radians(point1.lon / 1.0e7)
    lat2 = math.radians(point2.lat / 1.0e7)
    lon2 = math.radians(point2.lon / 1.0e7)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6378137 * c
