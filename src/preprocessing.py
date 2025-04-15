import numpy as np
import pandas as pd
from typing import Union

def load_data(
        path: str, year_min: int, year_max: int
) -> pd.DataFrame:
    df_raw = pd.read_csv(path)

    if year_min >= year_max:
        raise ValueError(f"{year_min=} must be (strictly) smaller than {year_max=}")

    df_raw["time"] = df_raw.time.astype("datetime64[us]")

    df_raw["year"] = df_raw.time.dt.year
    df_raw["month"] = df_raw.time.dt.month
    df_raw["day"] = df_raw.time.dt.day

    if year_max < np.min(df_raw["year"]):
        raise ValueError(f"{year_max=} is smaller than minimum observed year {np.min(df_raw['time'])}")
    if year_min < np.min(df_raw.year):
        print(f"Minimum year available in dataset is {np.min(df_raw.year)} and will be used as year_min.")
    if year_max > np.max(df_raw.year):
        print(f"Maximum year available in dataset is {np.max(df_raw.year)} and will be used as year_max.")

    df_filtered = df_raw[(df_raw["year"] >= year_min) & (df_raw["year"] <= year_max)].copy()

    return df_filtered


def resize_grid(
        df_weighted_avg: pd.DataFrame, lat_bnds_seq: list[Union[int, float]], gas: str
) -> pd.DataFrame:
    # duplicate each row as boundary latitudes enter multiple averages
    df_duplicate = pd.DataFrame(np.repeat(df_weighted_avg.values, len(lat_bnds_seq)-1, axis=0))
    df_duplicate.columns = df_weighted_avg.columns
    df_duplicate["bnds"] = list(range(len(lat_bnds_seq)-1))*int(len(df_duplicate)/(len(lat_bnds_seq)-1))

    # 'initialize' resized latitude bands
    df_duplicate["lat_bnd"] = None

    for i in range(len(lat_bnds_seq)-1):
        df_duplicate.loc[df_duplicate.lat_bnd.index, "lat_bnd"] = np.where(
            (df_duplicate.lat_bnds >= lat_bnds_seq[i]) & (df_duplicate.lat_bnds <= lat_bnds_seq[i+1]) &
            (df_duplicate.bnds==i%(len(lat_bnds_seq)-1)),
            f"{lat_bnds_seq[i]}-{lat_bnds_seq[i+1]}-N", df_duplicate.lat_bnd)

        df_duplicate.loc[df_duplicate.lat_bnd.index, "lat_bnd"] = np.where(
            (df_duplicate.lat_bnds <= lat_bnds_seq[i]) & (df_duplicate.lat_bnds >= (-1)*lat_bnds_seq[i+1]) &
            (df_duplicate.bnds==i%(len(lat_bnds_seq)-1)),
            f"{lat_bnds_seq[i]}-{lat_bnds_seq[i+1]}-S", df_duplicate.lat_bnd)

    df_gridded = df_duplicate.groupby(["year", "month", "day", "lat_bnd"]).agg(
        {f"x{gas}_weighted_avg":"mean"}
    ).reset_index()

    return df_gridded
