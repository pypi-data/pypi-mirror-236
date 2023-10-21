"""
lst_calendar.LSTCalendar
"""
from datetime import timedelta, datetime
from typing import Union, List
from .ObservationBlock import ObservationBlock
from .LSTCalendarDate import LSTCalendarDate
from .LSTInterval import LSTInterval
from ..idx import Idx, Interval
from ..utils import (
    normalize_yyyymmdd_to_datetime,
    normalize_coordinates,
    sun_stats,
    utc_to_lst,
    LST_DAY_DEC,
)


class LSTCalendar:
    """
    Calendar tailored for LST (Local Sidereal Time) related interval lookups.

    Attributes
    ----------
    start : datetime
        The beginning of the date range for the calendar.
    end : datetime
        The conclusion of the date range for the calendar.
    latitude : float
        The geographic latitude in decimal degrees. Defaults to 0.
    longitude : float
        The geographic longitude in decimal degrees. Defaults to 0.
    lst_calendar_index : Idx
        An index to manage intervals efficiently.
    dates : List[LSTCalendarDate]
        A list containing dates and corresponding sun statistics within the range.

    Methods
    -------
    __init__(start, end, latitude=0, longitude=0)
        Initialize the LSTCalendar object.
    _calculate_intervals(today_dt, today_sun, tomorrow_sun)
        Calculate intervals for a given date based on sun statistics.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(
        self,
        start: Union[str, datetime],
        end: Union[str, datetime],
        latitude: Union[str, float] = 0,
        longitude: Union[str, float] = 0,
    ):
        """
        Initialize the LSTCalendar object.

        Parameters
        ----------
        start : Union[str, datetime]
            Start date of the calendar range.
        end : Union[str, datetime]
            End date of the calendar range.
        latitude : Union[str, float], optional
            Latitude for the location. Defaults to 0.
        longitude : Union[str, float], optional
            Longitude for the location. Defaults to 0.

        Raises
        ------
        ValueError
            If the start date is after the end date.
        """
        start = normalize_yyyymmdd_to_datetime(start)
        end = normalize_yyyymmdd_to_datetime(end)

        if start > end:
            raise ValueError("start day should be <= end day")

        latitude, longitude = normalize_coordinates(latitude, longitude)
        self.latitude = latitude
        self.longitude = longitude
        self.lst_calendar_index = Idx()
        self.lst_block_index = Idx()
        self._observation_blocks: List["ObservationBlock"] = []

        # For caching the 'tomorrow' sun, relative to current day
        # This allows for sun_stats(..) to be called once per day,
        # Instead of once for today/tomorrow for every day
        _sun = None

        self.dates = []
        for d in range(0, (end - start).days + 1):
            dt = start + timedelta(days=d)
            sun = sun_stats(self.latitude, self.longitude, dt)
            tomorrow_sun = (
                sun_stats(self.latitude, self.longitude, dt + timedelta(days=1))
                if _sun is None
                else _sun
            )

            intervals = self._calculate_intervals(dt, dt + timedelta(days=1), sun, tomorrow_sun)
            for interval in intervals:
                self.lst_calendar_index.insert(interval)

            self.dates.append(LSTCalendarDate(dt, sun, intervals, self))

    @property
    def observation_blocks(self) -> List["ObservationBlock"]:
        return self._observation_blocks

    @observation_blocks.setter
    def observation_blocks(self, blocks: List["ObservationBlock"] = None):
        if blocks is None:
            blocks = []
        self._observation_blocks = blocks
        for block in blocks:
            block.calendar = self
            self.lst_block_index.insert(
                Interval(block.lst_window_start, block.lst_window_end, block)
            )

    def _calculate_intervals(self, today_dt, tomorrow_dt, today_sun, tomorrow_sun):
        """
        Calculate intervals for a given date based on sun statistics.

        Parameters
        ----------
        today_dt : datetime
            The specific day for which intervals are being calculated.
        today_sun : Dict
            The sun statistics for the specific day.

        Returns
        -------
        List[Interval]
            A list of calculated intervals.
        """
        today = today_dt
        today_lst = utc_to_lst(today.isoformat(), self.latitude, self.longitude)
        tomorrow = tomorrow_dt
        tomorrow_lst = utc_to_lst(tomorrow.isoformat(), self.latitude, self.longitude)
        today_dawn = today_sun.get("dawn")
        today_dawn_lst = utc_to_lst(today_dawn, self.latitude, self.longitude)
        today_sunrise = today_sun.get("sunrise")
        today_sunrise_lst = utc_to_lst(today_sunrise, self.latitude, self.longitude)
        today_sunset = today_sun.get("sunset")
        today_sunset_lst = utc_to_lst(today_sunset, self.latitude, self.longitude)
        today_dusk = today_sun.get("dusk")
        today_dusk_lst = utc_to_lst(today_dusk, self.latitude, self.longitude)
        tomorrow_dawn = tomorrow_sun.get("dawn")
        tomorrow_dawn_lst = utc_to_lst(tomorrow_dawn, self.latitude, self.longitude)
        tomorrow_dawn_lst = (
            tomorrow_dawn_lst + LST_DAY_DEC
            if (tomorrow_dawn_lst - today_dawn_lst) < (LST_DAY_DEC / 2)
            else tomorrow_dawn_lst
        )
        tomorrow_sunrise = tomorrow_sun.get("sunrise")
        tomorrow_sunrise_lst = (
            utc_to_lst(tomorrow_sunrise, self.latitude, self.longitude) + LST_DAY_DEC
        )
        tomorrow_sunrise_lst = (
            tomorrow_sunrise_lst + LST_DAY_DEC
            if (tomorrow_sunrise_lst - today_sunrise_lst) < (LST_DAY_DEC / 2)
            else tomorrow_sunrise_lst
        )
        tomorrow_sunset = tomorrow_sun.get("sunset")
        tomorrow_sunset_lst = utc_to_lst(tomorrow_sunset, self.latitude, self.longitude)
        tomorrow_sunset_lst = (
            tomorrow_sunset_lst + LST_DAY_DEC
            if (tomorrow_sunset_lst - today_sunset_lst) < (LST_DAY_DEC / 2)
            else tomorrow_sunset_lst
        )

        return [
            # AVOID_SUNRISE
            Interval(
                today_sunrise_lst,
                tomorrow_sunrise_lst,
                {
                    "sun": today_sun,
                    "dt": today,
                    "type": LSTInterval.AVOID_SUNRISE,
                    "solar_0": today_sunrise,
                    "solar_1": tomorrow_sunrise,
                },
            ),
            # AVOID_SUNSET
            Interval(
                today_sunset_lst,
                tomorrow_sunset_lst,
                {
                    "sun": today_sun,
                    "dt": today,
                    "type": LSTInterval.AVOID_SUNSET,
                    "solar_0": today_sunset,
                    "solar_1": tomorrow_sunset,
                },
            ),
            # AVOID_SUNRISE_SUNSET (1/2): sunrise - sunset
            Interval(
                today_sunrise_lst,
                today_sunset_lst + LST_DAY_DEC
                if today_sunset_lst < today_sunrise_lst
                else today_sunset_lst,
                {
                    "sun": today_sun,
                    "dt": today,
                    "type": LSTInterval.AVOID_SUNRISE_SUNSET,
                    "solar_0": today_sunrise,
                    "solar_1": today_sunset,
                },
            ),
            # AVOID_SUNRISE_SUNSET (2/2): sunset - sunrise
            Interval(
                today_sunset_lst,
                tomorrow_sunrise_lst,
                {
                    "sun": today_sun,
                    "dt": today,
                    "type": LSTInterval.AVOID_SUNRISE_SUNSET,
                    "solar_0": today_sunset,
                    "solar_1": tomorrow_sunrise,
                },
            ),
            # NIGHT_ONLY
            Interval(
                today_dusk_lst,
                tomorrow_dawn_lst,
                {
                    "sun": today_sun,
                    "dt": today,
                    "type": LSTInterval.NIGHT_ONLY,
                    "solar_0": today_dusk,
                    "solar_1": tomorrow_dawn,
                },
            ),
            # ALL_DAY
            Interval(
                today_lst,
                tomorrow_lst,
                {
                    "sun": today_sun,
                    "dt": today,
                    "type": LSTInterval.ALL_DAY,
                    "solar_0": today,
                    "solar_1": tomorrow,
                },
            ),
        ]
