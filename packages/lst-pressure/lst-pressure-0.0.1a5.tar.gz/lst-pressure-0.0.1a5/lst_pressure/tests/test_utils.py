from datetime import date, datetime
import pytest
from lst_pressure.utils.normalize_date import normalize_datetime, normalize_yyyymmdd_to_datetime
from lst_pressure.utils.normalize_coordinates import normalize_coordinates
from lst_pressure.utils.sun import sun_stats
from lst_pressure.utils.time_conversions import lst_to_utc, utc_to_lst


test_data = [
    {
        "time_conversion": {
            "utc": "2022-06-17 05:03:23.350528+00:00",
            "lst": "2022-06-17 0.18210963685182396 hourangle",
            "lat": "-30:42:39.8",
            "long": "21:26:38.0",
        },
        "yyyymmdd": ["20220617", date(2022, 6, 17)],
        "sunrise_sunset": {
            "dawn": "2022-06-17 05:03:23.350528+00:00",
            "sunrise": "2022-06-17 05:30:29.628263+00:00",
            "noon": "2022-06-17 10:35:03+00:00",
            "sunset": "2022-06-17 15:39:46.364401+00:00",
            "dusk": "2022-06-17 16:06:52.665164+00:00",
        },
        "lat": ["-30:42:39.8", -30.711055555555554],
        "long": ["21:26:38.0", 21.44388888888889],
    }
]


def test_normalize_datetime():
    d1_s = "2023-12-20 00:00:00"
    d1 = normalize_datetime(d1_s)
    d2 = datetime(2023, 12, 20, 0, 0, 0)
    assert isinstance(d1, datetime)
    assert d1 == d2
    assert normalize_datetime(d2) == d2


@pytest.mark.parametrize("test", test_data)
def test_lst_to_utc(test):
    time_conversion = test.get("time_conversion")
    utc_expected = normalize_datetime(time_conversion.get("utc"))
    lst = time_conversion.get("lst")
    long = time_conversion.get("long")
    lat = time_conversion.get("lat")
    utc = lst_to_utc(lst, lat, long)
    assert utc_expected.strftime("%Y-%m-%d %H:%M") == utc.strftime("%Y-%m-%d %H:%M")


@pytest.mark.parametrize("test", test_data)
def test_utc_to_lst(test):
    time_conversion = test.get("time_conversion")
    utc = time_conversion.get("utc")
    lst_expected = time_conversion.get("lst")
    long = time_conversion.get("long")
    lat = time_conversion.get("lat")
    lst = utc_to_lst(utc, lat, long, True)
    assert lst == lst_expected


@pytest.mark.parametrize("test", test_data)
def test_normalize_date(test):
    d = test["yyyymmdd"]
    assert normalize_yyyymmdd_to_datetime(d[0]) == d[1]
    assert normalize_yyyymmdd_to_datetime(d[1]) == d[1]


@pytest.mark.parametrize("test", test_data)
def test_normalize_coordinates(test):
    lat = test["lat"]
    long = test["long"]

    # Conversion of DMS should work
    lat_, long_ = normalize_coordinates(lat[0], long[0])
    assert lat_ == lat[1]
    assert long_ == long[1]

    # Using decimal degrees directly should also work
    lat_, long_ = normalize_coordinates(lat[1], long[1])
    assert lat_ == lat[1]
    assert long_ == long[1]

    # Should not be possible to use both DEC and DMS
    with pytest.raises(ValueError):
        normalize_coordinates(lat[0], long[1])
    with pytest.raises(ValueError):
        normalize_coordinates(lat[1], long[0])


@pytest.mark.parametrize("test", test_data)
def test_calc_sun(test):
    lat = test.get("lat")[0]
    long = test.get("long")[0]
    yyyymmdd = test.get("yyyymmdd")[1]
    sun = test.get("sunrise_sunset")
    expected = {key: datetime.fromisoformat(value) for key, value in sun.items()}

    result = sun_stats(lat, long, yyyymmdd)
    assert all(result.get(key) == value for key, value in expected.items())
