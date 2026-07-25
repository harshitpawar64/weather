from datetime import datetime, timedelta, timezone

from weather.models import UnixTimestamp


def parse_datetime(time_str: str, utc_offset_seconds: int) -> datetime:
    return datetime.fromisoformat(time_str).replace(
        tzinfo=timezone(timedelta(seconds=utc_offset_seconds))
    )


def calculate_valid_until(local_dt: datetime, interval: int) -> UnixTimestamp:
    return UnixTimestamp(local_dt.timestamp() + interval)
