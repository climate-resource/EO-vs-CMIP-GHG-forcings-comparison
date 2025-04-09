"""
analyse missing data for cimp7 and obs4mips comparison
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def compare_missing_data(
        d_cimp: pd.DataFrame,
        d_obs: pd.DataFrame,
        gas: str,
        min_year_cimp: int = 2002
) -> pd.DataFrame:
    """
    compute data frame with information about missing data

    comparing cimp7 with obs4mips for entire timeseries (2002-2023) and
    all latitudinal bands (-90 to 90)

    Parameters
    ----------
    d_cimp
        dataframe with cimp7 data

    d_obs
        dataframe with obs4mips data

    gas
        ghg variable, either ch4 or co2

    min_year_cimp
        minimum year for cimp7 data

    Returns
    -------
     :
        dataframe with information about missing data

    """
    d_cimp["time"] = d_cimp.time.astype("datetime64[us]")
    d_cimp = d_cimp[d_cimp.time.dt.year > min_year_cimp].copy()
    d_cimp["year_month"] = d_cimp["time"].dt.to_period("M")

    # load and prepare obs4mips data
    d_obs["time"] = d_obs.time.astype("datetime64[ns]")
    d_obs["year_month"] = d_obs['time'].dt.to_period('M')

    # select relevant columns
    d_obs2 = d_obs[
        ["lat_bnds", gas, "time", "year_month", f"x{gas}_nobs"]
    ].drop_duplicates().reset_index()

    d_cimp2 = d_cimp[
        ["lat_bnds", gas, "time", "year_month"]
    ].drop_duplicates().reset_index()

    d_obs_counts = d_obs2.groupby(
        ["lat_bnds", "year_month", f"x{gas}_nobs"]
    ).agg(
        {gas: "count"}
    ).reset_index(
    ).rename(
        columns={gas: f"{gas}_obs"}
    )

    d_cimp_counts = d_cimp2.groupby(
        ["lat_bnds", "year_month"]
    ).agg(
        {gas: "count"}
    ).reset_index(
    ).rename(
        columns={gas: f"{gas}_cimp"}
    )

    counts = pd.merge(
        d_obs_counts,
        d_cimp_counts,
        how="outer"
    )

    counts["missings"] = np.where(
        np.isnan(counts[f"{gas}_obs"]) | np.isnan(counts[f"{gas}_cimp"]),
        "True", "False"
    )
    return counts


def plot_missing(
        counts: pd.DataFrame,
        gas: str,
        **kwargs
) -> None:
    """
    plot missing data when comparing cimp7 and obs4mips

    Parameters
    ----------
    counts
        preprocessed dataframe with informaiton about
        missing data

    gas
        ghg variable, either ch4 or co2

    """
    fig, axs = plt.subplots(constrained_layout=True, **kwargs)
    sns.scatterplot(
        x=counts.year_month.astype(str),
        y=counts.lat_bnds.astype(str),
        hue=counts.missings,
        ax=axs,
        marker="s",
        edgecolor=None
    )
    ticks = axs.get_xticks()
    axs.set_xticks(ticks[::12])
    axs.tick_params(axis='x', rotation=45, labelsize=7)
    axs.tick_params(axis='y', labelsize=10)
    axs.legend(fontsize=7, loc="center right", labelspacing=0.1,
               handletextpad=0.2)
    axs.set_ylabel("latitudinal band")
    axs.set_xlabel("time (year-month)")
    axs.set_title(f"Missing data: Comparison of {gas} from CIMP7 and OBS4MIPS")
    plt.show()
