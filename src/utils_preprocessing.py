"""
helper functions for preparing data for src
"""

import pandas as pd
import numpy as np
from typing import Optional

def get_grid(
        df: pd.DataFrame,
        grid_deg: Optional[int],
        deg_only: Optional[list[int]]
) -> pd.DataFrame:
    """
    compute new latitude grid

    Parameters
    ----------
    df
        raw dataframe

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
        df2 = df[df.lat_bnds.isin(deg_only)].reset_index(drop=True)
        df2["lat_new"] = df2.lat_bnds
        return df2
    if grid_deg is not None:
        for i,j in zip(np.arange(0, 90, grid_deg), np.arange(grid_deg, 90.1, grid_deg)):
            df.loc[df[(df.lat > i) & (df.lat < j)].index, "lat_new"] = j
            df.loc[df[(df.lat < -i) & (df.lat > -j)].index, "lat_new"] = -j
        return df

def compute_cosine_weights(
        df_gridded: pd.DataFrame,
        ghg_gas: str
) -> pd.DataFrame:
    """
    compute cosine weighted ghg based on new latitude grid

    Parameters
    ----------
    df_gridded
        dataframe with new latitude grid column 'lat_new'

    ghg_gas
        ghg variable, either ch4 or co2

    Returns
    -------
    :
        dataframe with cosine weighted ghg column `{ghg_gas}_cos`
        and cosine weights in column 'cos_weights_lat'
    """
    df_gridded["cos_weights_lat"] = np.cos(np.deg2rad(df_gridded.lat))

    df_gridded[f"{ghg_gas}_cos"] = np.multiply(df_gridded[ghg_gas], df_gridded.cos_weights_lat)

    return df_gridded

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
    df_grouped = compute_cosine_weights(
        df_filtered, ghg_gas
    ).groupby("time").agg({f"{ghg_gas}_cos": "mean"}).reset_index()
    return df_grouped

def filter_year_range(
        df: pd.DataFrame,
        year_min: Optional[int],
        year_max: Optional[int]
) -> pd.DataFrame:
    """
    filter dataframe according to selected range of years

    Parameters
    ----------
    df
        raw dataframe

    year_min
        minimum year

    year_max
        maximum year

    Returns
    -------
    df_filtered :
        filtered dataframe according to selected range of years
    """
    if year_min is None:
        year_min = np.min(df.time.dt.year)
    if year_max is None:
        year_max = np.max(df.time.dt.year)

    df_filtered = df.where(
        (df.time.dt.year >= year_min) & (df.time.dt.year <= year_max)
    )
    return df_filtered

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
        df: pd.DataFrame,
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
    df
        raw dataframe

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
        preprocessed dataframe ready for src

    df_global_mean :
        averaged over all latitudes
    """
    df["time"] = df.time.astype("datetime64[us]")
    # select range of years
    df_filtered = filter_year_range(df, year_min, year_max)

    # grid dataframe
    df_gridded = get_grid(df_filtered, grid_deg, deg_only)

    df_grouped = compute_cosine_weights(
        df_gridded, ghg_gas
    ).groupby(["time", "lat_new"]).agg({f"{ghg_gas}_cos": "mean"}).reset_index()

    # if degree 90 is used change name to corresponding hemisphere
    # for easier interpretation
    df_plotting = adjust_lat_for_plotting(df_grouped)

    df_global_mean = compute_global_mean(df, ghg_gas, year_min, year_max)

    return df_plotting, df_global_mean


