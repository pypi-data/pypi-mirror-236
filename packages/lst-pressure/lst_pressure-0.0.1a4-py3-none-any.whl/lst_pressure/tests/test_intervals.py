import pytest
from lst_pressure.lst_calendar import LSTCalendar, LSTInterval, ObservationBlock


tests = [
    {
        "latlng": ["-30:42:39.8", "21:26:38.0"],
        "calendar": ["20231018", "20231019"],
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
                    "lst_window_start": 8.15,
                    "lst_window_end": 11.5,
                    "utc_constraints": [LSTInterval.AVOID_SUNRISE_SUNSET],
                },
                {"id": "obs-2", "lst_window_start": 1, "lst_window_end": 8},
                {
                    "id": "obs-3",
                    "lst_window_start": 22,
                    "lst_window_end": 22.5,
                    "utc_constraints": [LSTInterval.NIGHT_ONLY],
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
            observable_dates = block.observable_dates()

        # Get blocks that can be scheduled on a date
        for date in cal.dates:
            observable_blocks = date.observable_blocks()
            print("\n", observable_blocks)
