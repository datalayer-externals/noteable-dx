import numpy as np
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython.testing import tools

from dx.settings import get_settings

settings = get_settings()


@pytest.fixture
def get_ipython() -> TerminalInteractiveShell:
    if TerminalInteractiveShell._instance:
        return TerminalInteractiveShell.instance()

    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "col_1": list("aaa"),
            "col_2": list("bbb"),
            "col_3": list("ccc"),
        }
    )
    return df


@pytest.fixture
def sample_large_dataframe() -> pd.DataFrame:
    """
    Generates a dataframe that is within the MAX_ROWS/MAX_COLUMNS limits,
    but has large values that should still exceed MAX_RENDER_SIZE_BYTES.
    """
    large_values = ["A" * 1_000 for _ in range(settings.DISPLAY_MAX_ROWS)]

    df = pd.DataFrame()
    for i in range(settings.DISPLAY_MAX_COLUMNS):
        df[f"col_{i}"] = large_values
    return df


@pytest.fixture
def sample_long_dataframe() -> pd.DataFrame:
    num_rows = settings.DISPLAY_MAX_ROWS + 10
    return pd.DataFrame(np.random.rand(num_rows, 1))


@pytest.fixture
def sample_wide_dataframe() -> pd.DataFrame:
    num_cols = settings.DISPLAY_MAX_COLUMNS + 10
    return pd.DataFrame(np.random.rand(1, num_cols))


@pytest.fixture
def sample_long_wide_dataframe() -> pd.DataFrame:
    num_rows = settings.DISPLAY_MAX_ROWS + 10
    num_cols = settings.DISPLAY_MAX_COLUMNS + 10
    return pd.DataFrame(np.random.rand(num_rows, num_cols))