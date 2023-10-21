"""
lst_pressure.time_conversions
"""
from astropy.time import Time
from astropy import units as u
from astropy.utils import iers
from .normalize_coordinates import normalize_coordinates
from .normalize_date import normalize_datetime

iers.conf.auto_download = False
iers.conf.auto_max_age = None
iers.conf.iers_degraded_accuracy = "warn"

LST_DAY_DEC = 23.9344696
"""Length of a sideral day in decimal."""


def lst_to_utc(lst_str, lat, long):
    """lst_to_utc"""
    lat, long = normalize_coordinates(lat, long)

    # Extract date and LST hourangle from the string
    date_str, lst_hourangle, _ = lst_str.split()
    lst_decimal_hours = float(lst_hourangle)

    # Convert the decimal hours to hours, minutes, and seconds
    lst_hours = int(lst_decimal_hours)
    lst_minutes = int((lst_decimal_hours - lst_hours) * 60)
    lst_seconds = (lst_decimal_hours - lst_hours - lst_minutes / 60) * 3600

    # Set a starting UTC time at the beginning of the specified date
    start_utc = Time(f"{date_str} 00:00:00")

    # Find the UTC time that matches provided LST
    for i in range(0, (24 * 60 * 60), 5):  # Assuming a 5-second step size; adjust as needed
        test_utc = start_utc + i * u.second
        test_lst = test_utc.sidereal_time("mean", longitude=long).hour
        if (
            abs(test_lst - lst_hours - lst_minutes / 60 - lst_seconds / 3600) < 1 / 720
        ):  # Within 5 seconds (I think)
            return normalize_datetime(test_utc.iso)

    # If no match is found
    return None


def utc_to_lst(iso_date, lat, long, return_str_with_utc=False):
    """
    utc_to_lst
    """
    lat, long = normalize_coordinates(lat, long)
    t = Time(normalize_datetime(iso_date))
    lst = t.sidereal_time("mean", longitude=long)
    if return_str_with_utc:
        return f"{t.datetime.date()} {lst}"
    return lst.to_value()
