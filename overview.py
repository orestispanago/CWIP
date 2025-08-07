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


for wind_file in wind_files:
    print(wind_file)
    wind = read_wind_csv(wind_file)

    seed_locations = wind[
        (wind["seed-a [cnt]"].diff() > 0) | (wind["seed-b [cnt]"].diff() > 0)
    ]

    resampled = resample_1s(wind)
    # plot_flight_multi_timeseries_with_seed_vlines(resampled, seed_locations)

    resampled = resampled[
        resampled["lon [deg]"] > 30
    ]  # Sometimes GPS first location is out of KSA
    if len(resampled) > 0:
        aircraft = resampled.iloc[:, -1].dropna().values[0]
        start_timestamp = resampled.index[0]
        date_time = start_timestamp.strftime("%Y%m%d_%H%M%S")
        plot_plane_track_with_seeds(
            resampled,
            start_timestamp,
            aircraft,
            filename=f"plots/maps/flights/{date_time}_{aircraft}.png",
        )
    else:
        print(f"File: {wind_file} contains no values after filtering")
