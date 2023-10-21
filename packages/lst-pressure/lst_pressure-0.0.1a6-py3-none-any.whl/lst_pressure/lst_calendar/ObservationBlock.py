"""
lst_calendar.ObservationBlock
"""

from typing import List, Optional
from intervaltree import Interval
from ..lst_calendar import LSTCalendar, LSTInterval, LSTCalendarDate


class ObservationBlock:
    """
    Represents an observation block with given Local Sidereal Time (LST) window and UTC constraints.

    Attributes
    ----------
    id: any
        The ID of the observation block
    lst_window_start : float
        The starting value of the LST window.
    lst_window_end : float
        The ending value of the LST window.
    utc_constraints : List[LSTInterval]
        The UTC constraints for the observation block represented as a list of LSTInterval values. Defaults to 0.
    """

    def __init__(
        self,
        id: any,
        lst_window_start: float,
        lst_window_end: float,
        utc_constraints: List["LSTInterval"] = None,
    ):
        """
        Initializes an instance of ObservationBlock.

        Parameters
        ----------
        id: any
            The ID of the observation block
        lst_window_start : float
            The starting value of the LST window.
        lst_window_end : float
            The ending value of the LST window.
        utc_constraints : List[LSTInterval]
            The UTC constraints for the observation block represented as a list of LSTInterval values. Defaults to 0.
        """
        self.id = id
        self.lst_window_start = lst_window_start
        self.lst_window_end = lst_window_end
        self.utc_constraints = utc_constraints
        self._cal: Optional["LSTCalendar"] = None  # Reference to the calendar

    @property
    def calendar(self) -> "LSTCalendar":
        if not self._cal:
            raise ValueError("ObservationBlock has not been added to any LSTCalendar.")
        return self._cal

    @calendar.setter
    def calendar(self, cal: "LSTCalendar"):
        self._cal = cal

    def observable_dates(self) -> List["LSTCalendarDate"]:
        if not self._cal:
            raise ValueError("ObservationBlock has not been added to any LSTCalendar.")

        return [
            i
            for i in self.calendar.lst_calendar_index.get_intervals_containing(
                Interval(self.lst_window_start, self.lst_window_end)
            )
            if self.utc_constraints is None
            or (len(self.utc_constraints) > 0 and i[2]["type"] in self.utc_constraints)
        ]
