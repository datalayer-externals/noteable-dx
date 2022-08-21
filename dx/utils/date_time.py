import datetime

import numpy as np
import pandas as pd
import structlog

from dx.settings import get_settings

settings = get_settings()
logger = structlog.get_logger(__name__)


def generate_datetime_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            (
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")
            ).to_pydatetime()
            for _ in range(num_rows)
        ]
    )


def generate_time_period_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            (
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")
            ).to_period(freq="W")
            for _ in range(num_rows)
        ]
    )


def generate_time_interval_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            pd.Interval(
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 0)} hours"),
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(0, 1000)} hours"),
            )
            for _ in range(num_rows)
        ]
    )


def generate_time_delta_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours") for _ in range(num_rows)]
    )


def handle_time_period_series(s: pd.Series) -> pd.Series:
    types = (pd.Period, pd.PeriodIndex)
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has pd.Period values; converting to string")
        s = s.apply(lambda x: [x.start_time, x.end_time] if isinstance(x, types) else x)
    return s


def handle_time_delta_series(s: pd.Series) -> pd.Series:
    types = (
        datetime.timedelta,
        np.timedelta64,
        pd.Timedelta,
    )
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has pd.TimeDelta values; converting to total seconds")
        s = s.apply(lambda x: x.total_seconds() if isinstance(x, types) else x)
    return s