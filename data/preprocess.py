import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import nc_time_axis

df_obs = pd.read_csv("data/OBS4MIPS_CH4_prep.csv")
ds = xr.open_dataset("data/CMIP7_CH4.nc", use_cftime=True)
da = ds.ch4

year_slice = ["2002-01-15 00:00:00", "2022-01-15 00:00:00"]
lat_slice = [
#    [-37.5, -22.5],
#    [-22.5, -7.5],
    [-7.5, 7.5],
#    [7.5, 22.5],
#    [22.5, 37.5]
]
lat_bnd = [0] # [-30, -15, 0, 15, 30]

da_list = []
for lat_sl in lat_slice:
    da = ds.ch4.sel(lat=slice(lat_sl[0], lat_sl[1]),
                    time=slice(year_slice[0], year_slice[1]))

    weights = np.cos(np.deg2rad(da.lat))
    weights.name = "weights"
    lat_new_weighted = da.weighted(weights)
    mean_cos = lat_new_weighted.mean("lat")
    da_list.append(mean_cos)

da2 = xr.concat(da_list, dim="lat")
da2["time"] = da2.indexes['time'].to_datetimeindex()
df = da2.to_dataframe().reset_index()

df.replace({i: lat_bnd[i] for i in range(len(lat_bnd))}, inplace=True)
df["source"]="cimp7"
df["time"] = df.time.astype("datetime64[ns]")
df["year_month"] = df.time.dt.to_period("M")



obs_list = []
for i,lat_sl in enumerate(lat_slice):
    df_obs2 = df_obs[df_obs.lat.isin(lat_sl)][["time", "ch4"]]
    df_obs2["lat"]= i
    obs_list.append(df_obs2)

df2 = pd.concat(obs_list).drop_duplicates().reset_index(drop=True)
df2.replace({i: lat_bnd[i] for i in range(len(lat_bnd))}, inplace=True)
df2["source"]="obs4mips"
df2["time"] = df2.time.astype("datetime64[ns]")
df2["year_month"] = df2.time.dt.to_period('M')
df3 = df2.groupby(["year_month", "lat", "source"]).agg({"ch4":"mean"}).reset_index()

df_all = pd.concat([df[["year_month", "lat", "source", "ch4"]],
                    df3])

sns.lineplot(x=df_all.year_month.astype(str),
             y=df_all.ch4,
             hue=df_all.lat,
             style=df_all.source)
plt.show()
