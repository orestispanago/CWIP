import glob
from data_readers import read_wind_csv
from plotting_flight_maps import plot_plane_track_with_seeds
from plotting_flight_timeseries import (
    plot_flight_multi_timeseries_with_seed_vlines,
)
from utils import resample_1s, select_seed_locations

wind_files = glob.glob("*/*/*/*/*wind.csv")


for wind_file in wind_files:
    print(wind_file)
    wind = read_wind_csv(wind_file)

    seed_locations = select_seed_locations(wind)

    resampled = resample_1s(wind)
    plot_flight_multi_timeseries_with_seed_vlines(resampled, seed_locations)

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
