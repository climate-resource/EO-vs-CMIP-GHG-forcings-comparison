import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def combined_dataset(d1, d2, gas):
    d1["time"] = d1.time.astype("datetime64[us]")
    d1["year_month"] = d1["time"].dt.to_period("M")

    d2["time"] = d2.time.astype("datetime64[ns]")
    d2["year_month"] = d2['time'].dt.to_period('M')

    d1_agg = d1.groupby(["year_month", "lat_bnds"]).agg({gas: "mean"}).reset_index()
    d2_agg = d2.groupby(["year_month", "lat_bnds", f"x{gas}_nobs"]).agg({gas: "mean"}).reset_index()
    d2_agg.rename(columns={gas: f"x{gas}"}, inplace=True)

    d_combined = pd.merge(d1_agg, d2_agg, how="outer")
    return d_combined


def compare_monthly_coverage(d_combined, gas):
    d_combined["coverage_overlap"] = True
    d_combined.loc[(d_combined[gas].isnull()) | (d_combined[f"x{gas}"].isnull()),
    "coverage_overlap"] = False

    return d_combined


def plot_coverage(
        df_filtered: pd.DataFrame,
        gas: str,
        **kwargs
) -> None:
    fig, axs = plt.subplots(constrained_layout=True, **kwargs)
    sns.scatterplot(
        x=df_filtered.year_month.astype(str),
        y=df_filtered.lat_bnds.astype(str),
        ax=axs,
        hue=df_filtered[f"x{gas}_nobs"],
        marker="s",
        edgecolor=None
    )
    ticks = axs.get_xticks()
    axs.set_xticks(ticks[::12])
    axs.tick_params(axis='x', rotation=45, labelsize=7)
    axs.tick_params(axis='y', labelsize=10)
    axs.legend(title="xch4 nobs" ,fontsize=7, loc="center right", labelspacing=0.1,
               handletextpad=0.2)
    axs.set_ylabel("latitudinal band")
    axs.set_xlabel("time (year-month)")
    axs.set_title(f"Coverage: Comparison of {gas} from CMIP7 and OBS4MIPS")
    plt.show()
