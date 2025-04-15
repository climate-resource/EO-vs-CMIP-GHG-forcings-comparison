"""
helper functions for preparing data for src
"""
import xarray as xr
import pandas as pd
from typing import Optional
from old.src.cosine_weighting import weight_and_average

def get_grid(
        ds: xr.Dataset,
        grid_deg: Optional[int],
        deg_only: Optional[list[int]]
) -> pd.DataFrame:
    """
    compute new latitude grid

    Parameters
    ----------
    ds
        xarray dataset

    grid_deg
        in which degree steps should latitudes be gridded?
        possible values are 15, 30, 45, 90 or None
        if None, deg_only has to be specified

    deg_only
        select one specific latitudinal degree
        possible values are +/- 15, 30, 45, 90 or None
        if None, grid_deg has to be specified

    Returns
    -------
    :
        dataframe with new latitude grid column 'lat_new'
    """
    assert grid_deg in [15, 30, 45, 90, None], (
        f"grid_deg must be one of 15, 30, 45, 90, or None. Got {grid_deg=}"
    )
    assert (deg_only is None) ^ (grid_deg is None), (
        "either deg_only XOR grid_deg has to be specified"
    )

    if deg_only is not None:
        ds2 = ds.where(ds.lat_bnds.isin(deg_only), drop=True)
        ds2["lat_new"] = ds2.lat_bnds
        return ds2

    if grid_deg is not None:
        return ds


def compute_global_mean(
        df: pd.DataFrame,
        ghg_gas: str,
        year_min: Optional[int],
        year_max: Optional[int]
) -> pd.DataFrame:
    """
    compute global mean ghg based on new latitude grid

    Parameters
    ----------
    df_gridded
        gridded dataframe

    ghg_gas
        ghg variable, either ch4 or co2

    year_min
        minimum year that should be selected from raw data

    year_max
        maximum year that should be selected from raw data

    Returns
    -------
    df_grouped :
        dataframe with global mean ghg and time column
    """
    df["time"] = df.time.astype("datetime64[us]")
    # select range of years
    df_filtered = filter_year_range(df, year_min, year_max)
    breakpoint()
    df_grouped = compute_cosine_weights(
        df_filtered, ghg_gas
    ).groupby("time").agg({f"{ghg_gas}_cos": "mean"}).reset_index()
    return df_grouped



def adjust_lat_for_plotting(
        df_grouped: pd.DataFrame
) -> pd.DataFrame:

    df_grouped["lat_new"] = df_grouped.lat_new.astype(str)
    if len(df_grouped.lat_new.unique()) == 2:
        if all(df_grouped.lat_new.unique() == [str(-90.), str(90.)]):
            df_grouped.loc[
                df_grouped[df_grouped.lat_new == str(-90.)].index, "lat_new"
            ] = "southern"
            df_grouped.loc[
                df_grouped[df_grouped.lat_new == str(90.)].index, "lat_new"
            ] = "northern"

    return df_grouped

def prepare_data(
        ds,
        grid_deg: Optional[int] = None,
        deg_only: Optional[int] = None,
        ghg_gas: str = "ch4",
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
) -> tuple[pd.DataFrame]:
    """
    preprocess dataframe for src

    Parameters
    ----------
    ds
        raw xarray dataset

    grid_deg
        in which degree steps should latitudes be gridded?
        possible values are 15, 30, 45, 90 or None
        if None deg_only has to be specified

    deg_only
        which latitudinal degree should be used
        possible values are +/- 15, 30, 45, 90 or None
        if None grid_deg has to be specified

    ghg_gas
        ghg variable, either ch4 or co2

    year_min
        minimum year that should be selected from raw data

    year_max
        maximum year that should be selected from raw data

    Returns
    -------
    df_plotting :
        preprocessed dataframe ready for plotting

    df_global_mean :
        averaged over all latitudes
    """
    ds_filtered = ds.sel(time=slice(year_min, year_max))

    # grid dataframe
    ds_gridded = get_grid(ds_filtered, grid_deg, deg_only)

    if ghg_gas == "ch4":
        ds_grouped = weight_and_average(ds_gridded.ch4, weight_method="cosine")
    else:
        ds_grouped = weight_and_average(ds_gridded.co2, weight_method="cosine")

    ds_gridded["ch4"] = ds_grouped

    df_grouped = ds_gridded.to_dataframe().reset_index()

    # if degree 90 is used change name to corresponding hemisphere
    # for easier interpretation
    df_plotting = adjust_lat_for_plotting(df_grouped)

    #df_global_mean = compute_global_mean(df, ghg_gas, year_min, year_max)

    return df_plotting #, df_global_mean


