"""
calendar
"""
from datetime import datetime, timedelta


def generate_calendar(start_day, end_day):
    """fn"""
    start = datetime.strptime(start_day, "%Y%m%d")
    end = datetime.strptime(end_day, "%Y%m%d")

    if start > end:
        raise ValueError("Start day should be before or equal to end day.")

    return [(start + timedelta(days=x)) for x in range(0, (end - start).days + 1)]


__all__ = ["generate_calendar"]
