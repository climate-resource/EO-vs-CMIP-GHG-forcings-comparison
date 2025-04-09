"""
prepare datasets for comparison between CIMP7 ground-based and
OBS4MIPS satellite data
"""

import pandas as pd


def preprocess_obs4mips_data(
        d_raw: pd.DataFrame,
        gas: str,
        fill_value: float=1e+20,
        unit_factor: float=1e9
) -> pd.DataFrame:
    """
    create dataformat convenient for comparison

    Parameters
    ----------
    d_raw
        raw dataframe as downloaded from CDS

    gas
        ghg variable, either "ch4" or "co2"

    fill_value
        value used to specify missing values

    unit_factor
        scaling factor for converting ghg
        variable into desired unit

    Returns
    -------
    :
        preprocessed dataframe
    """
    # filter only rows with valid data
    d = d_raw[d_raw[f"x{gas}"] != fill_value].copy()
    # rescale unit to ppm
    d[gas] = d[f"x{gas}"]*unit_factor
    # set correct time format
    d["time"] = pd.to_datetime(d.time)
    # restructure latitudinal bands to make range
    # compatible with CIMP7 data
    lat_mapping_north = [
        ([-5., 0., 5.], 0),
        ([10., 15., 20.], 15),
        ([25., 30., 35.], 30),
        ([40., 45., 50.], 45),
        ([55., 60., 65.], 60),
        ([70., 75., 80.], 75),
        ([85.], 90),
    ]

    lat_mapping_south = [
        ([-1 * x for x in sublist], (-1)*second_value)
        for sublist, second_value in lat_mapping_north
    ]

    lat_mapping = lat_mapping_south+lat_mapping_north

    for old_lat, new_lat in lat_mapping:
        d.loc[d[d.lat_bnds.isin(old_lat)].index, "lat_bnds"] = new_lat

    # select relevant columns
    d_final = d[["time","lat_bnds", gas, f"x{gas}_nobs", "lat"]].reset_index()
    return d_final


data_ch4_obs4mips = preprocess_obs4mips_data(
    d_raw=pd.read_csv("data/OBS4MIPS_CH4.csv"),
    gas="ch4",
    fill_value=1e+20,
    unit_factor=1e9,
)


data_co2_obs4mips = preprocess_obs4mips_data(
    d_raw=pd.read_csv("data/OBS4MIPS_CO2.csv"),
    gas="co2",
    fill_value=1e+20,
    unit_factor=1e6,
)

data_ch4_obs4mips.to_csv("data/OBS4MIPS_CH4_prep.csv", index=False)
data_co2_obs4mips.to_csv("data/OBS4MIPS_CO2_prep.csv", index=False)