import xarray as xr
import os
import pandas as pd

path_CH4 = "C:/Users/FlorenceBockting/.esgpull/data/input4MIPs/CMIP7/CMIP/CR/CR-CMIP-1-0-0/atmos/mon/ch4/gnz/v20250228"
path_CO2 = "C:/Users/FlorenceBockting/.esgpull/data/input4MIPs/CMIP7/CMIP/CR/CR-CMIP-1-0-0/atmos/mon/co2/gnz/v20250228"

files_CH4 = os.listdir(path_CH4)
files_CO2 = os.listdir(path_CO2)

ds = []
for file in files_CH4:
    ds.append(xr.open_dataset(path_CH4+"/"+file).to_dataframe())

pd.merge(ds)