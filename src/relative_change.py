import numpy as np
import pandas as pd


def compute_change_to_baseline(df_combined: pd.DataFrame, gas: str, baseline_year: int = 2003):
    # prepare baseline year (= 2003)
    baseline = df_combined[df_combined.year_month.str.startswith(str(baseline_year))].melt(
        id_vars=("year_month", "lat_bnd"), value_vars=("cmip7", "obs4mips"),
        value_name=f"x{gas}_weighted_avg"
    ).groupby(
        ["year_month", "source"]
    ).agg(
        {f"x{gas}_weighted_avg": "mean"}
    ).reset_index(
    ).pivot(
        index="year_month", columns="source", values=f"x{gas}_weighted_avg"
    ).reset_index()

    # prepare remaining data
    global_mean_years = df_combined.melt(
        id_vars=("year_month", "lat_bnd"),
        value_vars=("cmip7", "obs4mips"),
        value_name=f"x{gas}_weighted_avg"
    ).groupby(
        ["year_month", "source"]
    ).agg(
        {f"x{gas}_weighted_avg": "mean"}
    ).reset_index()

    # compute relative change compare to baseline
    relative_change_months = []

    # compare ghg value month-wise
    for i in range(1,13):
        global_mean_month = global_mean_years[global_mean_years.year_month.str.endswith(f"_{i}")].pivot(
            index="year_month", columns="source", values=f"x{gas}_weighted_avg"
        ).reset_index()

        # broadcast baseline year to same number of rows as total dataset
        baseline_broadcasted = pd.DataFrame(
            np.repeat(
                baseline[baseline.year_month.str.endswith(f"_{i}")],
                len(global_mean_month),
                axis=0)
        )
        baseline_broadcasted.columns = baseline.columns

        # relative change in %
        df_relative_change_month = np.divide(
            global_mean_month[["cmip7", "obs4mips"]],
            baseline_broadcasted[["cmip7", "obs4mips"]]
        )*100

        df_relative_change_month["year_month"] = global_mean_month[
            global_mean_month.year_month.str.endswith(f"_{i}")
        ].year_month.unique()

        # combine all month-wise results
        relative_change_months.append(df_relative_change_month)

    df_relative_change = pd.concat(
        relative_change_months
    ).melt(
        id_vars="year_month",
        value_vars = ("cmip7", "obs4mips"),
        value_name=f"x{gas}_weighted_avg"
    ).reset_index()

    df_relative_change.loc[
        df_relative_change.year_month.index, "year_month_time"
    ] = pd.to_datetime(
        df_relative_change['year_month'],
        format='%Y_%m'
    )

    return df_relative_change
