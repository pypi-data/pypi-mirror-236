from ..lst_calendar import LSTCalendar


def test_Calendar():
    assert ["20220101", "20220102", "20220103", "20220104", "20220105"] == [
        d.dt.strftime("%Y%m%d") for d in LSTCalendar("20220101", "20220105").dates
    ]
