from src.preprocessing import (
    load_data,
    resize_grid
)
from src.cosine_weighting import (
    compute_weighted_ghg,
    compute_weighted_average_latitude_bands
)
import numpy as np
import pytest


@pytest.mark.parametrize(
    "gas, unit_factor, fill_value",
    [("ch4", 1e9, 1e20), ("co2", 1e6, 1e20)]
)
def test_resize_grid(gas, unit_factor, fill_value):
    path = f"data/OBS4MIPS_{gas.upper()}.csv"
    year_min=2002
    year_max=2023

    df_obs4mips = load_data(path, year_min=year_min, year_max=year_max)

    df_obs4mips_weighted = compute_weighted_ghg(df_obs4mips, gas=gas, unit_factor=unit_factor)

    df_obs4mips_weighted_avg = compute_weighted_average_latitude_bands(
        df_obs4mips_weighted, gas=gas
    )

    df_obs4mips_new_grid = resize_grid(
        df_obs4mips_weighted_avg, lat_bnds_seq=[0, 30, 60, 90], gas="ch4"
    )

    np.testing.assert_array_equal(
        df_obs4mips_new_grid.lat_bnd.unique().astype(set),
        {'60-90-S', '30-60-S', '0-30-S', '0-30-N', '30-60-N', '60-90-N'}
    )
