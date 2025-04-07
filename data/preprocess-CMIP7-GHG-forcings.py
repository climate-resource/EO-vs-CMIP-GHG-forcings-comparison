import xarray as xr
import os
import pandas as pd

path_CH4 = "C:/Users/FlorenceBockting/.esgpull/data/input4MIPs/CMIP7/CMIP/CR/CR-CMIP-1-0-0/atmos/mon/ch4/gnz/v20250228"
path_CO2 = "C:/Users/FlorenceBockting/.esgpull/data/input4MIPs/CMIP7/CMIP/CR/CR-CMIP-1-0-0/atmos/mon/co2/gnz/v20250228"

files_CH4 = os.listdir(path_CH4)
files_CO2 = os.listdir(path_CO2)

def create_dataset(gas):
    if gas == "CH4":
        files = files_CH4
        path = path_CH4
    elif gas == "CO2":
        files = files_CO2
        path = path_CO2
    else:
        raise ValueError("Gas must be CH4 or CO2")

    ds = []
    for file in files:
        ds.append(xr.open_dataset(path + "/" + file).to_dataframe())

    pd.concat(ds).to_csv(f"data/CMIP7_{gas}.csv")


create_dataset("CH4")
create_dataset("CO2")