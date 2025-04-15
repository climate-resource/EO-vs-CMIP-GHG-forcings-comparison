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
    "gas, cmip_data, unit_factor, fill_value, cell_size",
    [
        ("ch4", False, 1e9, 1e20, 5), # obs4mips
        ("co2", False, 1e6, 1e20, 5), # obs4mips
        ("ch4", True, None, None, 15), # cmip7
        ("co2", True, None, None, 15)  # cmip7
     ]
)
def test_resize_grid(
        gas, cmip_data, unit_factor, fill_value, cell_size
):
    if cmip_data:
        path = f"data/CMIP7_{gas.upper()}.csv"
    else:
        path = f"data/OBS4MIPS_{gas.upper()}.csv"

    year_min=2002
    year_max=2023

    df = load_data(
        path, year_min=year_min, year_max=year_max
    )

    df_weighted = compute_weighted_ghg(
        df, gas=gas, unit_factor=unit_factor, cmip_data=cmip_data, cell_size=cell_size
    )

    df_weighted_avg = compute_weighted_average_latitude_bands(
        df_weighted, gas=gas
    )

    df_new_grid = resize_grid(
        df_weighted_avg, lat_bnds_seq=[0, 30, 60, 90], gas=gas
    )

    np.testing.assert_array_equal(
        set(df_new_grid.lat_bnd.unique()),
        {'60-90-S', '30-60-S', '0-30-S', '0-30-N', '30-60-N', '60-90-N'}
    )
