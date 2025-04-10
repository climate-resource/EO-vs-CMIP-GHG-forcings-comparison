"""
helper functions for src
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_data(
        df_prep: pd.DataFrame,
        ghg_gas: str,
        global_mean: bool
) -> None:
    """
    plot data

    Parameters
    ----------
    df_prep
        preprocessed dataframe

    ghg_gas
        ghg variable, either ch4 or co2

    global_mean
        whether global mean should be plotted

    """
    plt.style.use("seaborn-v0_8-whitegrid")

    if ghg_gas == "ch4":
        unit="ppb"
        name=r"$CH_4$"
    else:
        unit="ppm"
        name=r"$CO_2$"

    fig, ax = plt.subplots(figsize=(7,4))

    df_plotting, df_global_mean = df_prep

    if len(np.unique(df_plotting.lat_new)) == 1:
        sns.lineplot(data=df_plotting, x="time", y=f"{ghg_gas}_cos",
                     label=df_plotting.lat_new[0], ax=ax)

    else:
        sns.lineplot(data=df_plotting, x="time", y=f"{ghg_gas}_cos", hue="lat_new",
                     palette="icefire", ax=ax)

    if global_mean:
        sns.lineplot(data=df_global_mean, x="time", y=f"{ghg_gas}_cos", linestyle="dashed",
                     color="black", ax=ax, label="global mean")

    ax.legend(handlelength=0.4, ncol=2, frameon=False, title="latitude",
              fontsize="medium")

    ax.spines[['right', 'top']].set_visible(False)
    ax.set_xlabel("year")
    ax.set_ylabel(name+f" in {unit} (cosine-weighted)")
    plt.title("data source: CMIP7 v1.0.0")
    plt.show()
