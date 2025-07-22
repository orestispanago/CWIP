import glob
import pandas as pd
from readers import read_wind_csv
from plotting import *

wind_files = glob.glob("*/*/*/*/*wind.csv")


def resample_1s(df):
    numeric_cols = df.select_dtypes(include="number").columns
    string_cols = df.select_dtypes(exclude="number").columns
    # Resample numeric and string parts separately
    numeric_resampled = df[numeric_cols].resample("1s").mean()
    string_resampled = df[string_cols].resample("1s").first()  # or .last()
    # Combine them back
    return pd.concat([numeric_resampled, string_resampled], axis=1)


for wind_file in wind_files[2:3]:

    wind = read_wind_csv(wind_file)

    seed_locations = wind[
        (wind["seed-a [cnt]"].diff() > 0)
        | (wind["seed-b [cnt]"].diff() > 0)
    ]

    resampled = resample_1s(wind)
    plot_flight_multi_timeseries_with_seed_vlines(resampled, seed_locations)
    
    # resampled = resampled[resampled["lon [deg]"]>30] # Sometimes GPS first location is out of KSA
    # if len(resampled) >0:
    #     plot_plane_track_with_seeds(resampled)
    # else:
    #     print(f"File: {flight} contains no values after filtering")

    # 2D track with seed events in different color

    # Detect cloud penetrations based on LWC
    # flag as pen_seed and pen_noseed
