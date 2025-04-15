import numpy as np
import pandas as pd

def compute_weighted_ghg(
        df: pd.DataFrame, gas:str, unit_factor: float, cmip_data:bool, fill_values:float=1e20, cell_size: int=5
) -> pd.DataFrame:
    if not cmip_data:
        # step 1: prepare the data
        df_filtered = df[df[f"x{gas}"] != fill_values].reset_index(drop=True)
        df_filtered[f"x{gas}"] = df_filtered[f"x{gas}"] * unit_factor

        # step 2: average over longitudes
        df_lat = df_filtered.groupby(
            ["year", "month", "day", "year_month" ,"bnds", "lat", "lat_bnds"]
        ).agg({f"x{gas}": "mean"}).reset_index()

    else:
        df_lat = df
        df_lat.rename(columns={f"{gas}": f"x{gas}"}, inplace=True)

    # step 3: compute weights wrt bounding latitudes and compute weighted ghg variable
    df_lat.loc[df_lat.lat.index, "delta_phi"] = abs(np.subtract(
        np.sin(df_lat.lat + (cell_size/2)), # upper bounding latitude
        np.sin(df_lat.lat - (cell_size/2))  # lower bounding latitude
    ))
    df_lat[f"x{gas}_weighted"] = df_lat[f"x{gas}"].multiply(df_lat.delta_phi)

    return df_lat


def compute_weighted_average_latitude_bands(
        df_weighted: pd.DataFrame, gas: str
) -> pd.DataFrame:
    # step 4: compute weighted average over latitudes to get a value for each latitude bound
    df_lat_avg = df_weighted.groupby(
        ["year", "month", "day", "year_month","lat_bnds"]
    ).agg(
        {f"x{gas}_weighted": "sum", "delta_phi": "sum"}
    ).reset_index()

    df_lat_avg.loc[df_lat_avg.index, f"x{gas}_weighted_avg"] = df_lat_avg[f"x{gas}_weighted"]/df_lat_avg.delta_phi
    return df_lat_avg