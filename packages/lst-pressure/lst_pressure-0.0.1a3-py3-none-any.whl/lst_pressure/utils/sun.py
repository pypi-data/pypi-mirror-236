"""
sun.py
"""
from astral.sun import sun
from astral import LocationInfo
from .normalize_coordinates import normalize_coordinates
from .normalize_date import normalize_yyyymmdd_to_datetime


def sun_stats(latitude, longitude, yyyymmdd):
    """Calculate sun-related stats of a calendar day at UTC"""
    latitude, longitude = normalize_coordinates(latitude, longitude)
    dt = normalize_yyyymmdd_to_datetime(yyyymmdd)
    location = LocationInfo(latitude=latitude, longitude=longitude)
    return sun(location.observer, date=dt)
