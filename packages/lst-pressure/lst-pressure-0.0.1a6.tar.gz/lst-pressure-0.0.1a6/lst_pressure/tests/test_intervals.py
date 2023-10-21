import pytest
from lst_pressure.lst_calendar import LSTCalendar, LSTInterval, ObservationBlock


tests = [
    {
        "latlng": ["-30:42:39.8", "21:26:38.0"],
        "calendar": ["20230901", "20231019"],
        "observation_blocks": [
            ObservationBlock(
                id=block.get("id"),
                lst_window_start=block.get("lst_window_start"),
                lst_window_end=block.get("lst_window_end"),
                utc_constraints=block.get("utc_constraints"),
            )
            for block in [
                {
                    "id": "obs-1",
                    "lst_window_start": 12,
                    "lst_window_end": 14,
                    "utc_constraints": [LSTInterval.AVOID_SUNSET],
                },
                {
                    "id": "obs-2",
                    "lst_window_start": 7,
                    "lst_window_end": 8.1,
                    "utc_constraints": [LSTInterval.AVOID_SUNSET],
                },
                {
                    "id": "obs-3",
                    "lst_window_start": 10,
                    "lst_window_end": 14,
                    "utc_constraints": [LSTInterval.AVOID_SUNSET],
                },
            ]
        ],
    }
]


@pytest.mark.parametrize("test", tests)
def test_observations(test):
    start, end = test.get("calendar")
    latitude, longitude = test.get("latlng")

    with LSTCalendar(start, end, latitude, longitude) as cal:
        cal.observation_blocks = test.get("observation_blocks")

        # Get dates a block can be scheduled on
        for block in cal.observation_blocks:
            dates = block.observable_dates()

        # Get blocks that can be observed on a date
        for date in cal.dates:
            interval_blocks = date.observable_blocks()
            print(date.dt, len(interval_blocks[0].get("blocks")))
