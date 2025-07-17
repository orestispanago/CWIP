import glob
import pandas as pd
from plotting import *

flights = glob.glob("*/*/*/*/")


def resample_1s(df):
    numeric_cols = df.select_dtypes(include="number").columns
    string_cols = df.select_dtypes(exclude="number").columns
    # Resample numeric and string parts separately
    numeric_resampled = df[numeric_cols].resample("1s").mean()
    string_resampled = df[string_cols].resample("1s").first()  # or .last()
    # Combine them back
    return pd.concat([numeric_resampled, string_resampled], axis=1)


for flight in flights:

    adc_fname = glob.glob(f"{flight}/*adc.csv")[0]
    fin_fname = glob.glob(f"{flight}/*fin.csv")[0]
    wind_fname = glob.glob(f"{flight}/*wind.csv")[0]

    fin = pd.read_csv(fin_fname, parse_dates=True, index_col="datetime")
    wind = pd.read_csv(wind_fname, parse_dates=True, index_col="datetime")
    adc = pd.read_csv(adc_fname, parse_dates=True, index_col="datetime")

    fin.index = fin.index.round("s")
    wind.index = wind.index = wind.index.round("s")

    fin = fin[~fin.index.duplicated(keep="first")]
    wind = wind[~wind.index.duplicated(keep="first")]

    merged = pd.concat([fin, wind], axis=1)

    seed_locations = merged[
        (merged["seed-a [cnt]"].diff() > 0)
        | (merged["seed-b [cnt]"].diff() > 0)
    ]

    resampled = resample_1s(merged)
    # plot_flight_multi_timeseries_with_seed_vlines(resampled, seed_locations)
    plot_plane_track_with_seeds(resampled)

    # 2D track with seed events in different color

    # Detect cloud penetrations based on LWC
    # flag as pen_seed and pen_noseed
