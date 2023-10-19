"""
test_calendar.py
"""
from . import generate_calendar


def test_generate_calendar():
    """fn"""
    start_day = "20220101"
    end_day = "20220105"
    calendar = [c.strftime("%Y%m%d") for c in generate_calendar(start_day, end_day)]
    assert calendar == ["20220101", "20220102", "20220103", "20220104", "20220105"]
