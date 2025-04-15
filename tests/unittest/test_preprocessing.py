from src.preprocessing import (
    load_data,
)

import numpy as np
import pandas as pd
import operator
import pytest


@pytest.mark.parametrize("path", ["data/OBS4MIPS_CH4.csv", "data/CMIP7_CH4.csv",
                                   "data/OBS4MIPS_CO2.csv", "data/CMIP7_CO2.csv"])
@pytest.mark.parametrize("year_min", [1990, 2003, 2010])
@pytest.mark.parametrize("year_max", [2002, 2023, 2030])
def test_load_data(path, year_min, year_max):

    df_raw = pd.read_csv(path)

    if (year_min >= year_max) or (year_max < np.min(df_raw.time.astype("datetime64[us]").dt.year)):
        np.testing.assert_raises(
            ValueError, load_data, path, year_min, year_max
        )

    else:
        df = load_data(path, year_min=year_min, year_max=year_max)

        if year_min < np.min(df.year):
           assert year_min != np.min(df.year)
           np.testing.assert_equal(np.min(df.year), np.min(df_raw.time.astype("datetime64[us]").dt.year))
        else:
            np.testing.assert_equal(year_min, np.min(df.year))

        if year_max > np.max(df.year):
            assert year_max != np.max(df.year)
            np.testing.assert_equal(np.max(df.year), np.max(df_raw.time.astype("datetime64[us]").dt.year))
        else:
            np.testing.assert_equal(year_max, np.max(df.year))

        np.testing.assert_equal(type(df), pd.DataFrame)
        np.testing.assert_array_compare(operator.__ne__, len(df), 0)