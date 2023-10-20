"""
lst_calendar.LSTInterval
"""

from enum import Enum


class LSTInterval(Enum):
    """
    Different types of LST intervals to avoid specific times of the day.

    Attributes
    ----------
    AVOID_SUNRISE : Enum
        Represents intervals that avoid sunrise.
    AVOID_SUNSET : Enum
        Represents intervals that avoid sunset.
    AVOID_SUNRISE_SUNSET : Enum
        Represents intervals that avoid both sunrise and sunset.
    NIGHT_ONLY : Enum
        Represents intervals that only consider night time.
    """

    AVOID_SUNRISE = 1
    AVOID_SUNSET = 2
    AVOID_SUNRISE_SUNSET = 3
    NIGHT_ONLY = 4
