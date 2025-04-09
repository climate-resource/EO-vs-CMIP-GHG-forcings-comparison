"""
Collect, merge, and save downloaded datasets as csv/nc
"""

import xarray as xr
import os

def create_dataset_from_CMIP7_data(gas: str) -> None:
    """
    create dataset from ghg data

    different datasets are merged and saved as
    csv and nc in folder /data

    Parameters
    ----------
    gas
        ghg variable, either CH4 or CO2
    """
    path_CH4 = "C:/Users/FlorenceBockting/.esgpull/data/input4MIPs/CMIP7/CMIP/CR/CR-CMIP-1-0-0/atmos/mon/ch4/gnz/v20250228"
    path_CO2 = "C:/Users/FlorenceBockting/.esgpull/data/input4MIPs/CMIP7/CMIP/CR/CR-CMIP-1-0-0/atmos/mon/co2/gnz/v20250228"

    files_CH4 = os.listdir(path_CH4)
    files_CO2 = os.listdir(path_CO2)

    if gas == "CH4":
        files = files_CH4
        path = path_CH4
    elif gas == "CO2":
        files = files_CO2
        path = path_CO2
    else:
        raise ValueError("Gas must be CH4 or CO2")

    ds_list = []
    for file in files:
        ds = xr.open_dataset(path + "/" + file, use_cftime=True)
        ds_list.append(ds)

    ds_combined = (xr.concat(ds_list, dim="time"))
    ds_combined.to_netcdf(f"data/CMIP7_{gas}.nc")
    ds_combined.to_dataframe().to_csv(f"data/CMIP7_{gas}.csv")


def create_dataset_from_OBS4MIPs(gas: str) -> None:
    """
    create dataset from OBS4MIPs ghg data

    Parameters
    ----------
    gas
        ghg variable, either CH4 or CO2

    """
    path = "C:/Users/FlorenceBockting/data/OBS4MIPs/"
    file_CH4 = "200301_202212-C3S-L3_XCH4-GHG_PRODUCTS-MERGED-MERGED-OBS4MIPS-MERGED-v4.5.nc"
    file_CO2 = "200301_202212-C3S-L3_XCO2-GHG_PRODUCTS-MERGED-MERGED-OBS4MIPS-MERGED-v4.5.nc"

    if gas == "CH4":
        file = file_CH4
    elif gas == "CO2":
        file = file_CO2
    else:
        raise ValueError("Gas must be CH4 or CO2")

    ds = xr.open_dataset(path + "/" + file)
    ds.to_dataframe().to_csv(f"data/OBS4MIPS_{gas}.csv")


create_dataset_from_CMIP7_data("CH4")
create_dataset_from_CMIP7_data("CO2")

create_dataset_from_OBS4MIPs("CH4")
create_dataset_from_OBS4MIPs("CO2")