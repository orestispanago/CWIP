import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.errors import EmptyDataError

from data_readers import read_wind_csv
from utils import select_seed_locations, resample_1s
from plotting_case_study import (
    plot_flight_timeseries_with_seed_and_penetration_vlines,
    plot_bar_pens_per_window,
    plot_boxplot_pens_seeds,
    plot_pen_window_timeseries,
    plot_seed_window_timeseries,
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
from plotting_flight_timeseries import (
    plot_flight_multi_timeseries_with_seed_vlines,
)
from plotting_case_study_map import plot_flight_track_with_pens_and_seeds



LWC_THRESHOLD = 0.3
WINDOW_SEC = 8
LWC_THRESHOLD_RANGE = np.arange(0.2, 1.0, 0.02)  # start, stop, step


def get_map_extent(df, offset=0.01):
    xmin = df["lon [deg]"].min() - offset
    xmax = df["lon [deg]"].max() + offset
    ymin = df["lat [deg]"].min() - offset
    ymax = df["lat [deg]"].max() + offset
    return [xmin, xmax, ymin, ymax]


def describe_time_windows(seeds, penetrations, pens_with_seed):
    description = {
        "seeds": len(seeds),
        "penetrations": len(penetrations),
        "penetrations with seeds": len(pens_with_seed),
    }
    return pd.DataFrame([description]).T


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


wind_file = (
    "split/Spring 2025/CS2/20250429051654/cwip_CS2_20250429051654_wind.csv"
)
wind_df = read_wind_csv(wind_file)

stem = os.path.basename(wind_file)[5:-9]
summary_df = calc_summary(wind_df, wind_file).T
summary_df.to_csv(f"out/case-study/{stem}_summary.csv", header=False)

seeds = select_seed_locations(wind_df)
seeds["seed_id"] = range(1, len(seeds) + 1)

pens = wind_df[wind_df["lwc [g/m^3]"] > LWC_THRESHOLD].copy()
pens["pen_id"] = range(1, len(pens) + 1)

# plot_flight_timeseries_with_seed_and_penetration_vlines(
#     wind_df, "lwc [g/m^3]", seeds, pens
# )

start_ts = wind_df.index[0]
dt_str = start_ts.strftime("%Y%m%d_%H%M%S")
aircraft = wind_df["aircraft"].iloc[0]


seed_extent = get_map_extent(pens, offset=0.025)
plot_flight_track_with_pens_and_seeds(
    wind_df,
    seeds,
    pens,
    extent=seed_extent,
    radar_label_offset=0.02,
    title=f"{aircraft}, {start_ts}",
    filename=f"plots/case-study/maps/pens-seeds/{aircraft}_{dt_str}.png",
)

import sys
sys.exit()


plot_flight_multi_timeseries_with_seed_vlines(
    wind_df,
    seeds,
    filename=f"plots/case-study/timeseries/all-flight/{aircraft}_{dt_str}.png",
)


if len(seeds) < 1:
    raise EmptyDataError(f"No seed events for {start_ts}, {aircraft}")

win_td = pd.Timedelta(seconds=WINDOW_SEC)
seed_windows_list = select_time_windows(wind_df, seeds, win_td)
pen_windows_list = select_time_windows(wind_df, pens, win_td)

seed_windows_df = time_windows_to_df(seed_windows_list)
pen_windows_df = time_windows_to_df(pen_windows_list)

seed_in_pen = pen_windows_df.loc[seeds.index]
# seed_in_pen = pd.merge(seeds, pen_windows_df, how="inner", on="datetime")
pens_with_seed_count = seed_in_pen["window_count"].value_counts().sort_index()
windows_description = describe_time_windows(seeds, pens, pens_with_seed_count)


plot_bar_pens_per_window(pens_with_seed_count)


# Plot each event
plot_pen_window_timeseries(seed_windows_list, aircraft, dt_str, "seed-event")
plot_seed_window_timeseries(pen_windows_list, aircraft, dt_str, "penetration")

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

plot_boxplot_pens_seeds(
    pens,
    seeds,
    dt_str,
    aircraft,
    title=f"{aircraft}, {start_ts}",
    filename=f"plots/case-study/boxplots/pen-vs-seed/{aircraft}/{aircraft}_{dt_str}_lwc.png",
)
