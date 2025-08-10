import pandas as pd
import glob
from data_readers import read_wind_csv
from utils import select_seed_locations, resample_1s, select_cloud_penetrations
from plotting_cloud_penetrations import (
    plot_flight_timeseries_with_seed_and_penetration_vlines,
)
from plotting_time_window import (
    plot_flight_boxplot_per_event,
    plot_boxplot_by_relative_time,
)
from utils_time_window import (
    select_time_windows,
    time_windows_to_df,
    to_relative_time_index,
)


wind_files = glob.glob("*/*/*/*/*wind.csv")
threshold = 0.3
window_seconds = 8
window_timedelta = pd.Timedelta(seconds=window_seconds)


all_seed_event_windows_rel_list = []
all_pen_windows_rel_list = []

for count, wind_file in enumerate(wind_files):
    print(wind_file)
    wind = read_wind_csv(wind_file)
    seed_locations = select_seed_locations(wind)
    penetrations = select_cloud_penetrations(wind)
    print(f"Cloud penetrations: {len(penetrations)}")
    print(f"Seed events: {len(seed_locations)}")

    resampled = resample_1s(wind)

    start_timestamp = resampled.index[0]
    date_time = start_timestamp.strftime("%Y%m%d_%H%M%S")
    aircraft = resampled.iloc[:, -1].values[0]

    resampled["diff"] = resampled["lwc [g/m^3]"].diff()

    # plot_flight_timeseries_lwc_diff_over_threshold(resampled, threshold)
    if len(penetrations) > 0:
        plot_flight_timeseries_with_seed_and_penetration_vlines(
            wind, "lwc [g/m^3]", seed_locations, penetrations
        )
        pen_windows = select_time_windows(wind, penetrations, window_timedelta)
        pen_windows_df = time_windows_to_df(pen_windows)
        # plot_flight_boxplot_per_event(
        #     pen_windows_df,
        #     "lwc [g/m^3]",
        #     start_timestamp,
        #     aircraft,
        #     window_seconds=window_seconds,
        #     xlabel="Cloud penetrations",
        #     filename=f"plots/boxplots/per-penetration/{date_time}_{aircraft}.png",
        # )
        pen_windows_rel = [to_relative_time_index(df) for df in pen_windows]
        pen_windows_df_rel = pd.concat(pen_windows_rel)
        all_pen_windows_rel_list.append(pen_windows_df_rel)
        # plot_boxplot_by_relative_time(
        #     pen_windows_df_rel,
        #     "lwc [g/m^3]",
        #     title=f"{start_timestamp}, {aircraft}",
        #     xlabel="Time relative to cloud penetration (s)",
        #     filename=f"plots/boxplots/by-penetration-relative-time/{date_time}_{aircraft}_lwc.png",
        # )
    else:
        print(f"No cloud penetrations for {start_timestamp}, {aircraft}")

# all_pen_windows_rel_df = pd.concat(all_pen_windows_rel_list)
# plot_boxplot_by_relative_time(
#     all_pen_windows_rel_df,
#     "lwc [g/m^3]",
#     xlabel="Time relative to cloud penetration (s)",
#     filename="plots/boxplots/all-flights/pen_lwc.png",
# )
# plot_boxplot_by_relative_time(
#     all_pen_windows_rel_df,
#     "rh [%]",
#     xlabel="Time relative to cloud penetration (s)",
#     filename="plots/boxplots/all-flights/pen_rh.png",
# )
# plot_boxplot_by_relative_time(
#     all_pen_windows_rel_df,
#     "wind_w [m/s]",
#     xlabel="Time relative to cloud penetration (s)",
#     filename="plots/boxplots/all-flights/pen_wind_w.png",
# )
# plot_boxplot_by_relative_time(
#     all_pen_windows_rel_df,
#     "ss_total [%]",
#     xlabel="Time relative to cloud penetration (s)",
#     filename="plots/boxplots/all-flights/pen_ss_total.png",
# )
