"""
lst_calendar.LSTCalendarDate
"""
from typing import List, Dict, Union
from intervaltree import Interval
from ..lst_calendar import LSTCalendar, ObservationBlock


class LSTCalendarDate:
    def __init__(self, dt, sun, intervals, cal) -> None:
        self.dt = dt
        self.sun = sun
        self.intervals = intervals
        self.calendar: "LSTCalendar" = cal

    def observable_blocks(self) -> List[Dict[str, Union["Interval", "ObservationBlock"]]]:
        results = []
        lst_block_index = self.calendar.lst_block_index
        for interval in self.intervals:
            block_intervals = lst_block_index.get_intervals_contained_by(interval)
            if block_intervals:
                results.append({"interval": interval, "blocks": [b[2] for b in block_intervals]})

        return results
