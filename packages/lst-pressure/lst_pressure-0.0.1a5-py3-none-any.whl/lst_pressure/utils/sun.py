"""
utils.sun
---------

This module is part of the `utils` package and provides utilities to compute
sun statistics based on given coordinates and date.
"""

from typing import Union
from astral.sun import sun
from astral import LocationInfo
from .normalize_coordinates import normalize_coordinates
from .normalize_date import normalize_yyyymmdd_to_datetime


def sun_stats(latitude: Union[float, str], longitude: Union[float, str], yyyymmdd: str) -> dict:
    """
    Calculate the sun's position statistics for a given location and date.

    Parameters
    ----------
    latitude : float or str
        Latitude of the location. Can be in various formats and will be normalized internally.
    longitude : float or str
        Longitude of the location. Can be in various formats and will be normalized internally.
    yyyymmdd : str
        Date in 'YYYYMMDD' format.

    Returns
    -------
    dict
        Dictionary containing the sun statistics such as sunrise, sunset, etc.

    Example
    -------
    >>> sun_stats("40.7128", "-74.0060", "20220101")
    {'dawn': ..., 'sunrise': ..., 'sunset': ..., ...}

    Notes
    -----
    This function uses the `astral` library to compute the sun statistics.
    The timezone is hardcoded to UTC.
    """
    latitude, longitude = normalize_coordinates(latitude, longitude)
    dt = normalize_yyyymmdd_to_datetime(yyyymmdd)
    location = LocationInfo(latitude=latitude, longitude=longitude)
    location.timezone = "UTC"
    return sun(location.observer, date=dt)
