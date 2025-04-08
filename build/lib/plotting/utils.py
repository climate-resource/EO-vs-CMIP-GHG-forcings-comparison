import pandas as pd
import xarray as xr
import numpy as np
from typing import Optional

def cosine_weighting(ds: xr.Dataset, gas:str = "ch4") -> xr.Dataset:
    """
    compute cosine weighted average

    Requires that the latitudinal dimension has the name
    'lat'

    Parameters
    ----------
    ds
        netcdf dataset

    Returns
    -------
    :
        netcdf dataset with cosine-weighted average
    """
    if gas == "ch4":
        ds_gas = ds.ch4
    elif gas == "co2":
        ds_gas = ds.co2
    else:
        raise ValueError(f"unknown gas {gas}")

    weights = np.cos(np.deg2rad(ds_gas.lat))
    gas_weighted = ds_gas.weighted(weights)
    weighted_mean = gas_weighted.mean("lat_bnds")
    ds[f"cos_weighted_{gas}"] = weighted_mean
    return ds


def prep_ds(
        ds: xr.Dataset, years: list[Optional[int]], number_lat_groups: int
) -> dict[[str], xr.Dataset]:
    if years[0] is None:
        years[0] = np.min(ds.time.dt.year)
    if years[1] is None:
        years[1] = np.max(ds.time.dt.year)

    ds_filtered = ds.where((ds.time.dt.year >= years[0]) & (ds.time.dt.year <= years[1]))

    ds_global_mean = ds_filtered.ch4.groupby("time").apply(cosine_weighting)
    ds_lat_grouped = ds_filtered.ch4.groupby("lat_bnds").apply(cosine_weighting)

    return dict(
        global_mean=ds_global_mean,
        group_by_lat=ds_lat_grouped,
    )