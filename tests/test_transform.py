import pandas as pd
import pytest

from transform import transform_weather_data


def make_raw_data(
    dates=None,
    temp_max=None,
    temp_min=None,
    precipitation=None,
):
    return {
        "city": "Mexico City",
        "daily": {
            "time": dates or ["2026-10-16", "2026-10-17"],
            "temperature_2m_max": temp_max or [23.0, 24.0],
            "temperature_2m_min": temp_min or [13.0, 14.0],
            "precipitation_sum": precipitation or [1.0, 2.0],
        },
    }


def test_transform_creates_expected_columns():
    raw_data = make_raw_data()

    df = transform_weather_data(raw_data)

    expected_columns = [
        "city",
        "date",
        "temp_max_c",
        "temp_min_c",
        "precipitation_mm",
    ]

    assert list(df.columns) == expected_columns
    assert len(df) == 2
    assert df["city"].unique().tolist() == ["Mexico City"]


def test_transform_converts_date_to_datetime():
    raw_data = make_raw_data()

    df = transform_weather_data(raw_data)

    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_transform_removes_null_values():
    raw_data = make_raw_data(
        dates=["2026-10-16", "2026-10-17"],
        temp_max=[23.0, None],
        temp_min=[13.0, 14.0],
        precipitation=[1.0, 2.0],
    )

    df = transform_weather_data(raw_data)

    assert len(df) == 1
    assert df["temp_max_c"].isnull().sum() == 0


def test_transform_rejects_duplicate_dates():
    raw_data = make_raw_data(
        dates=["2026-10-16", "2026-10-16"],
        temp_max=[23.0, 24.0],
        temp_min=[13.0, 14.0],
        precipitation=[1.0, 2.0],
    )

    with pytest.raises(ValueError, match="Duplicate dates"):
        transform_weather_data(raw_data)


def test_transform_rejects_invalid_temperature():
    raw_data = make_raw_data(
        dates=["2026-10-16"],
        temp_max=[10.0],
        temp_min=[20.0],
        precipitation=[1.0],
    )

    with pytest.raises(
        ValueError,
        match="Maximum temperature is lower than minimum temperature",
    ):
        transform_weather_data(raw_data)


def test_transform_rejects_negative_precipitation():
    raw_data = make_raw_data(
        dates=["2026-10-16"],
        temp_max=[23.0],
        temp_min=[13.0],
        precipitation=[-1.0],
    )

    with pytest.raises(
        ValueError,
        match="Precipitation cannot be negative",
    ):
        transform_weather_data(raw_data)


def test_transform_rejects_missing_daily_keys():
    raw_data = {
        "city": "Mexico City",
        "daily": {
            "time": ["2026-10-16"],
            "temperature_2m_max": [23.0],
        },
    }

    with pytest.raises(ValueError, match="Missing daily keys"):
        transform_weather_data(raw_data)