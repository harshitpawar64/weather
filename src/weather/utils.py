from datetime import datetime, timedelta, timezone

from weather.models import UnixTimestamp


def parse_datetime(time_str: str, utc_offset_seconds: int) -> datetime:
    return datetime.fromisoformat(time_str).replace(
        tzinfo=timezone(timedelta(seconds=utc_offset_seconds))
    )


def calculate_valid_until(local_dt: datetime, interval: int) -> UnixTimestamp:
    return UnixTimestamp(local_dt.timestamp() + interval)


def _calculate_us_aqi(
    c: float, breakpoints: list[tuple[float, float, float, float]]
) -> float:
    """
    I = [(I_high - I_low) / (C_high - C_low)] * (C - C_low) + I_low
    """
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= c <= c_high:
            return ((i_high - i_low) / (c_high - c_low)) * (c - c_low) + i_low

    c_low, c_high, i_low, i_high = breakpoints[-1]
    return ((i_high - i_low) / (c_high - c_low)) * (c - c_low) + i_low


def get_us_aqi(pm_2_5: float, pm_10: float) -> int:
    pm_2_5 = max(0.0, int(pm_2_5 * 10) / 10)
    pm_10 = max(0, int(pm_10))

    # (C_low, C_high, I_low, I_high)
    pm_2_5_breakpoints = [
        (0.0, 9.0, 0.0, 50.0),
        (9.1, 35.4, 51.0, 100.0),
        (35.5, 55.4, 101.0, 150.0),
        (55.5, 125.4, 151.0, 200.0),
        (125.5, 225.4, 201.0, 300.0),
        (225.5, 325.4, 301.0, 400.0),
        (325.5, 500.4, 401.0, 500.0),
    ]

    # (C_low, C_high, I_low, I_high)
    pm_10_breakpoints = [
        (0.0, 54.0, 0.0, 50.0),
        (55.0, 154.0, 51.0, 100.0),
        (155.0, 254.0, 101.0, 150.0),
        (255.0, 354.0, 151.0, 200.0),
        (355.0, 424.0, 201.0, 300.0),
        (425.0, 504.0, 301.0, 400.0),
        (505.0, 604.0, 401.0, 500.0),
    ]

    pm_2_5_aqi = _calculate_us_aqi(pm_2_5, pm_2_5_breakpoints)
    pm_10_aqi = _calculate_us_aqi(pm_10, pm_10_breakpoints)

    return round(max(pm_2_5_aqi, pm_10_aqi))
