import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ch4(df, years, **kwargs):
    df["time"] = [int(df.time_bnds.values[i][:4]) for i in range(len(df))]
    df = df[(df["time"] >= years[0]) & (df["time"] <= years[1])]
    df = df.groupby(["time_bnds", "lat_bnds"]).agg({"ch4": "mean"}).reset_index()
    df["lat_bnds"] = df["lat_bnds"].astype(str)

    fig, ax = plt.subplots(**kwargs)
    sns.lineplot(x="time_bnds", y="ch4", data=df, hue="lat_bnds", ax=ax,
                 palette="icefire")
    #ax.plot(df["time"], df["ch4"], "o")
    ax.legend(handlelength=0.4, ncol=3, frameon=False)
    plt.show()

years = [2002, 2022]
df = pd.read_csv("data/CMIP7_CH4.csv")

plot_ch4(df, years=[2002,2022], figsize=(6,4))
