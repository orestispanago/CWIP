import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.errors import EmptyDataError

from data_readers import read_wind_csv
from utils import select_seed_locations, get_index_middle, resample_1s
from plotting_cloud_penetrations import (
    plot_flight_timeseries_with_seed_and_penetration_vlines,
)
from utils_summary import calc_summary
from utils_time_window import (
    select_time_windows,
    time_windows_to_df,
    to_relative_time_index,
)
from plotting_time_window import (
    plot_boxplot_by_relative_time,
    plot_flight_boxplots_by_event,
    plot_multiple_timeseries,
)


LWC_THRESHOLD = 0.3
WINDOW_SEC = 8
LWC_THRESHOLD_RANGE = np.arange(0.2, 1.0, 0.02)  # start, stop, step


def plot_thresholds(wind, seed_locations):
    lwc_thresholds = np.arange(start=0.2, stop=1, step=0.02)
    pen_thresholds_dict_list = []
    for threshold in lwc_thresholds:
        penetration_count = len(wind[wind["lwc [g/m^3]"] > threshold])
        pen_thresholds_dict_list.append(
            {"lwc_threshold": threshold, "penetrations": penetration_count}
        )
    penetrations_per_threshold = pd.DataFrame(pen_thresholds_dict_list)
    print(penetrations_per_threshold)

    x = penetrations_per_threshold["lwc_threshold"]
    y = penetrations_per_threshold["penetrations"]
    plt.plot(x, y)
    plt.xlabel("lwc_threshold")
    plt.ylabel("penetrations")
    plt.axhline(len(seed_locations))
    plt.show()


def plot_event_timeseries(windows_list, aircraft, dt_str, event_type):
    """Plot multi-timeseries for each event window."""
    initials = event_type[:2]
    cols = [
        "lwc [g/m^3]",
        "rh [%]",
        "temp_amb [C]",
        "wind_w [m/s]",
        "ss_total [%]",
    ]
    for win in windows_list:
        event_id = win["window_count"].iloc[0]
        rel = to_relative_time_index(win)
        event_time = get_index_middle(win)
        plot_multiple_timeseries(
            rel,
            cols,
            xlabel=f"Time relative to {event_type} (s)",
            title=f"{aircraft}, {event_type} {event_id}: {event_time}",
            filename=(
                f"plots/case-study/timeseries/each-{event_type}/"
                f"{aircraft}/{aircraft}_{initials}{event_id:02}_{dt_str}_.png"
            ),
        )


wind_file = (
    "split/Spring 2025/CS2/20250429051654/cwip_CS2_20250429051654_wind.csv"
)
wind_df = read_wind_csv(wind_file)

stem = os.path.basename(wind_file)[5:-9]
summary_df = calc_summary(wind_df, wind_file).T
summary_df.to_csv(f"out/case-study/{stem}_summary.csv", header=False)

seeds = select_seed_locations(wind_df)
pens = wind_df[wind_df["lwc [g/m^3]"] > LWC_THRESHOLD]


plot_flight_timeseries_with_seed_and_penetration_vlines(
    wind_df, "lwc [g/m^3]", seeds, pens
)

resampled_wind_df = resample_1s(wind_df)
start_ts = resampled_wind_df.index[0]
dt_str = start_ts.strftime("%Y%m%d_%H%M%S")
aircraft = resampled_wind_df["aircraft"].iloc[0]

resampled_wind_df["diff"] = resampled_wind_df["lwc [g/m^3]"].diff()

if len(seeds) < 1:
    raise EmptyDataError(f"No seed events for {start_ts}, {aircraft}")

win_td = pd.Timedelta(seconds=WINDOW_SEC)
seed_windows_list = select_time_windows(wind_df, seeds, win_td)
pen_windows_list = select_time_windows(wind_df, pens, win_td)

seed_windows_df = time_windows_to_df(seed_windows_list)
pen_windows_df = time_windows_to_df(pen_windows_list)

# Plot each event
plot_event_timeseries(seed_windows_list, aircraft, dt_str, "seed-event")
plot_event_timeseries(pen_windows_list, aircraft, dt_str, "penetration")

seed_windows_rel_list = [to_relative_time_index(df) for df in seed_windows_list]
seed_windows_rel_df = pd.concat(seed_windows_rel_list)

pen_windows_rel_list = [to_relative_time_index(df) for df in pen_windows_list]
pen_windows_rel_df = pd.concat(pen_windows_rel_list)

# All events in one plot
plot_flight_boxplots_by_event(
    seed_windows_df,
    "lwc [g/m^3]",
    start_ts,
    aircraft,
    window_seconds=WINDOW_SEC,
    filename=(
        f"plots/case-study/boxplots/by-seed-event/{aircraft}/{aircraft}_{dt_str}.png"
    ),
    title=f"{aircraft}, {start_ts}, time window: {WINDOW_SEC} s",
)

plot_flight_boxplots_by_event(
    pen_windows_df,
    "lwc [g/m^3]",
    start_ts,
    aircraft,
    window_seconds=WINDOW_SEC,
    filename=(
        f"plots/case-study/boxplots/by-penetration/{aircraft}/{aircraft}_{dt_str}.png"
    ),
    xlabel="Cloud penetrations",
    title=f"{aircraft}, {start_ts}, time window: {WINDOW_SEC} s",
)

# Relative-time boxplots for each variable
cols = [
    "lwc [g/m^3]",
    "rh [%]",
    "temp_amb [C]",
    "ss_total [%]",
    "vel_down [m/s]",
    "accel_down [m/s^2]",
    "attack [deg]",
]
for col in cols:
    var_tag = col.split(" ")[0]

    plot_boxplot_by_relative_time(
        seed_windows_rel_df,
        col,
        title=f"{aircraft}, {start_ts}",
        filename=(
            f"plots/case-study/boxplots/by-seed-relative-time/{aircraft}/{aircraft}_{dt_str}_{var_tag}.png"
        ),
    )

    plot_boxplot_by_relative_time(
        pen_windows_rel_df,
        col,
        title=f"{aircraft}, {start_ts}",
        filename=(
            f"plots/case-study/boxplots/by-penetration-relative-time/{aircraft}/{aircraft}_{dt_str}_{var_tag}.png"
        ),
        xlabel="Time relative to cloud penetrations (s)",
    )
