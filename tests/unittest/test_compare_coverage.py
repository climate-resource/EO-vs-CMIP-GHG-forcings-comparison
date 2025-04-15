from old.src.utils import (
    compare_monthly_coverage,
    plot_coverage,
    combined_dataset
)
import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def d1():
    return pd.read_csv("data/CMIP7_CH4.csv")
@pytest.fixture
def d2():
    return pd.read_csv("data/OBS4MIPS_CH4_prep.csv")


def test_combined_dataset(d1, d2):
    gas="ch4"

    ds_combined = combined_dataset(
        d1, d2, gas=gas
    )

    np.testing.assert_array_equal(
        len(ds_combined.year_month.unique()),
        len(d1.year_month.unique())
    )


def test_compare_monthly_coverage(d1, d2):
    gas="ch4"

    ds_combined = combined_dataset(d1, d2, gas=gas)

    df = compare_monthly_coverage(ds_combined, gas=gas)
    df_filtered = df[df.coverage_overlap]

    np.testing.assert_array_equal(
        df_filtered.coverage_overlap, [True]*len(df_filtered)
    )


def test_coverage_plot(d1, d2):
    gas = "ch4"

    ds_combined = combined_dataset(d1, d2, gas=gas)

    df_coverage = compare_monthly_coverage(ds_combined, gas=gas)
    df_filtered = df_coverage[df_coverage.coverage_overlap]
    plot_coverage(df_filtered, gas=gas)

    df_filtered2 = df_filtered[df_filtered[f"x{gas}_nobs"] > 10]
    p = plot_coverage(df_filtered2, gas=gas)

    np.testing.assert_equal(p, None)

