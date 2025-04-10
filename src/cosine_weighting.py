import pandas as pd
import xarray as xr
import numpy as np


def weight_and_average(
        dataarray: xr.DataArray,
        weight_method: str,  # "cosine" or "unweighted"
) -> xr.DataArray:
    """
    Cosine weighting and averaging along the latitudes

    Parameters
    ----------
    dataarray
        data array of ghg variable

    weight_method
        either "cosine" or "unweighted"

    Returns
    -------
    :
        data array with cosine-weighted and averaged
        values of the ghg variable
    """
    if weight_method == "cosine":
        weights = np.cos(np.deg2rad(dataarray.lat))
    elif weight_method == "unweighted":
        weights = xr.ones_like(dataarray.lat)
    else:
        raise ValueError("weight_method must be either 'cosine' or 'unweighted'")

    weighted_array = dataarray.weighted(weights)
    return weighted_array.mean("lat")


def preprocessed_dataframe(
        ds: xr.Dataset,
        lat_slices: list,
        year_slices: list[str],
        weight_method: str = "cosine",  # or "unweighted"
) -> pd.DataFrame:
    """
    Prepares dataframe for plotting

    includes selecting time range, averaging over latitudes
    and averaging using cosine-weighting

    Parameters
    ----------
    ds
        Dataset of ghg variable

    lat_slices
        Array including latitude slices

    year_slices
        List with start and end year

    weight_method
        Which weighting method should be used? Either
        "cosine" or "unweighted"

    Returns
    -------
    :
        Dataframe of ghg variable
    """
    combine_latitude_slices = []
    for lat_slice in lat_slices:
        # filter relevant years
        ch4_date_range = ds.ch4.sel(
            lat=slice(lat_slice[0], lat_slice[1]),
            time=slice(year_slices[0], year_slices[1])
        )
        # weighted average along latitudes
        ch4_weighted_average = weight_and_average(
            ch4_date_range, weight_method=weight_method)
        ch4_weighted_average["lat_bnd"] = str(lat_slice)
        combine_latitude_slices.append(ch4_weighted_average)

    ch4_weighted_combined = xr.concat(
        combine_latitude_slices, dim="lat"
    )
    ch4_weighted_combined["time"] = ch4_weighted_combined.indexes['time'].to_datetimeindex()

    ch4_data_frame = ch4_weighted_combined.to_dataframe().reset_index()
    ch4_data_frame["time"] = ch4_data_frame.time.astype("datetime64[ns]")
    return ch4_data_frame
