import pandas as pd
import glob
from config import BOXPLOTS, SPLIT_DATA
from data_readers import read_wind_csv
from plotting_time_window import (
    plot_barplot_by_relative_time,
    plot_boxplot_by_relative_time,
    plot_flight_boxplots_by_event,
    plot_flight_timeseries_lwc_diff,
    plot_flight_timeseries_lwc_diff_over_threshold,
    plot_multiple_timeseries,
)

from utils.utils import resample_1s, select_seed_locations
from utils.time_window import (
    select_time_windows,
    time_windows_to_df,
    to_relative_time_index,
)


wind_files = glob.glob(f"{SPLIT_DATA}/**/*wind.csv", recursive=True)
threshold = 0.3
window_seconds = 8
window_timedelta = pd.Timedelta(seconds=window_seconds)

all_seed_event_windows_rel_list = []


for count, wind_file in enumerate(wind_files):
    print(wind_file)
    # for wind_file in wind_files[2:3]:
    wind = read_wind_csv(wind_file)
    seed_locations = select_seed_locations(wind)
    resampled = resample_1s(wind)

    start_timestamp = resampled.index[0]
    date_time = start_timestamp.strftime("%Y%m%d_%H%M%S")
    aircraft = resampled.iloc[:, -1].values[0]
    # plot_flight_timeseries_lwc_diff(resampled, threshold)

    resampled["diff"] = resampled["lwc [g/m^3]"].diff()

    # plot_flight_timeseries_lwc_diff_over_threshold(resampled, threshold)

    if len(seed_locations) > 0:
        seed_event_windows = select_time_windows(
            wind, seed_locations, window_timedelta
        )
        seed_event_windows_df = time_windows_to_df(seed_event_windows)
        # plot_flight_boxplots_by_event(
        #     seed_event_windows_df,
        #     "lwc [g/m^3]",
        #     start_timestamp,
        #     aircraft,
        #     window_seconds=window_seconds,
        #     filename=f"{BOXPLOTS}/per-seed-event/{date_time}_{aircraft}.png",
        # )

        # seed_event_example = to_relative_time_index(seed_event_windows[0])
        # plot_multiple_timeseries(seed_event_example, ["lwc [g/m^3]", "rh [%]","temp_amb [C]","wind_w [m/s]", "ss_total [%]"])

        seed_event_windows_rel = [
            to_relative_time_index(df) for df in seed_event_windows
        ]
        seed_event_windows_df_rel = pd.concat(seed_event_windows_rel)

        all_seed_event_windows_rel_list.append(seed_event_windows_df_rel)

        # plot_boxplot_by_relative_time(
        #     seed_event_windows_df_rel,
        #     "lwc [g/m^3]",
        #     title=f"{start_timestamp}, {aircraft}",
        #     filename=f"{BOXPLOTS}/by-seed-relative-time/{date_time}_{aircraft}_lwc.png",
        # )

    else:
        print(f"No seed events for {start_timestamp}, {aircraft}")

all_seed_event_windows_rel_df = pd.concat(all_seed_event_windows_rel_list)

plot_boxplot_by_relative_time(
    all_seed_event_windows_rel_df,
    "lwc [g/m^3]",
    title="All flights",
    filename=f"{BOXPLOTS}/all-flights/seed_lwc.png",
)
plot_boxplot_by_relative_time(
    all_seed_event_windows_rel_df,
    "rh [%]",
    title="All flights",
    filename=f"{BOXPLOTS}/all-flights/seed_rh.png",
)
plot_boxplot_by_relative_time(
    all_seed_event_windows_rel_df,
    "wind_w [m/s]",
    title="All flights",
    filename=f"{BOXPLOTS}/all-flights/seed_wind_w.png",
)
plot_boxplot_by_relative_time(
    all_seed_event_windows_rel_df,
    "ss_total [%]",
    title="All flights",
    filename=f"{BOXPLOTS}/all-flights/seed_ss_total.png",
)
