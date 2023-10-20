"""
lst_calendar.LSTCalendarDate
"""
from typing import List
from ..lst_calendar import LSTCalendar, ObservationBlock


class LSTCalendarDate:
    def __init__(self, dt, sun, intervals, cal) -> None:
        self.dt = dt
        self.sun = sun
        self.intervals = intervals
        self.calendar: "LSTCalendar" = cal

    def observable_blocks(self) -> List["ObservationBlock"]:
        return [
            dt_i
            for dt_i in self.intervals
            for observation_i in self.calendar.lst_block_index.get_intervals_contained_by(dt_i)
            if not observation_i[2].utc_constraints
            or dt_i[2].get("type") in observation_i[2].utc_constraints
        ]
