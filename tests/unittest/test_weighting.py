from src.preprocessing import load_data
from src.cosine_weighting import compute_weighted_ghg
import numpy as np
import pytest


@pytest.mark.parametrize(
    "gas, unit_factor, fill_value",
    [("ch4", 1e9, 1e20), ("co2", 1e6, 1e20)]
)
def test_weighting(gas, unit_factor, fill_value):
    path = f"data/OBS4MIPS_{gas.upper()}.csv"
    year_min = 2002
    year_max = 2023

    df_obs4mips = load_data(path, year_min=year_min, year_max=year_max)

    df_obs4mips_weighted = compute_weighted_ghg(df_obs4mips, gas=gas, unit_factor=unit_factor)

    np.testing.assert_equal(
        len(df_obs4mips_weighted), len(df_obs4mips)
    )