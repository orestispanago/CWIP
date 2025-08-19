import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.errors import EmptyDataError
import seaborn as sns

from data_readers import read_wind_csv
from utils.utils import select_seed_locations
from plotting_case_study import (
    plot_flight_timeseries_with_seed_and_penetration_vlines,
    plot_bar_pens_per_window,
    plot_boxplot_pens_seeds,
    plot_pen_window_timeseries,
    plot_seed_window_timeseries,
    plot_confusion_matrix_seed_or_pen,
    plot_barplot_penetrations,
    plot_barplot_seeds,
    plot_barplot_penetration_durations,
    plot_time_window_multi_timeseries_with_pens_and_vlines,
)
from utils.summary import calc_summary
from utils.time_window import (
    select_time_windows,
    time_windows_to_df,
    to_relative_time_index,
)
from plotting_time_window import (
    plot_boxplot_by_relative_time,
    plot_flight_boxplots_by_event,
    plot_multiple_timeseries,
)
from plotting_flight_timeseries import plot_flight_multi_timeseries_with_vlines
from plotting_maps_case_study import plot_flight_track_with_pens_and_seeds
from utils.plotting import MEDIUM_SIZE
from config import CS_BARPLOTS, CS_BOXPLOTS, CS_TIMESERIES, CS_MAPS, CS_TABLES

LWC_THRESHOLD = 0.3
WINDOW_SEC = 8


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


def compress_cloud_timeseries(df, max_nans_in_a_row=4):
    # Identify NaNs
    mask = df["cloud_id"].isna()
    # Create groups of consecutive values
    groups = (mask != mask.shift()).cumsum()
    # Count position inside each run
    nan_run_position = mask.groupby(groups).cumsum()
    # Keep rows where either not NaN OR NaN position ≤ 5
    df_filtered = df[~mask | (nan_run_position <= max_nans_in_a_row)]
    return df_filtered


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


# wind_file = "data/split/Spring 2025/CS02/20250429051654/cwip_CS02_20250429051654_wind.csv"
wind_file = "data/split/Spring 2025/CS04/20250429120855/cwip_CS04_20250429120855_wind.csv"

wind_df = read_wind_csv(wind_file)

start_ts = wind_df.index[0]
end_ts = wind_df.index[-1]
start_str = start_ts.strftime("%H:%M")
end_str = end_ts.strftime("%H:%M")
dt_str = start_ts.strftime("%Y%m%d_%H%M%S")
date = start_ts.strftime("%d/%m/%Y")
aircraft = wind_df["aircraft"].iloc[0]


cloud_mask = wind_df["lwc [g/m^3]"] > 0.3
flare_mask = (wind_df["seed-a [cnt]"].diff() > 0) | (
    wind_df["seed-b [cnt]"].diff() > 0
)
wind_df["is_in_cloud"] = cloud_mask
wind_df["flare_fired"] = flare_mask

in_cloud_ids = (cloud_mask != cloud_mask.shift()).cumsum()[cloud_mask]
in_cloud_ids = in_cloud_ids.factorize()[0] + 1  # 1, 2, 3, ...

in_cloud = wind_df[cloud_mask].assign(in_cloud_id=in_cloud_ids)

# in_cloud_or_flare_fired = wind_df[cloud_mask | flare_mask]
flares_in_cloud = wind_df[cloud_mask & flare_mask]

seeds = select_seed_locations(wind_df)
seeds["seed_id"] = range(1, len(seeds) + 1)


cloud_groups = (cloud_mask & ~cloud_mask.shift(fill_value=False)).cumsum()
wind_df["cloud_id"] = cloud_groups.mask(~cloud_mask).astype("Int64")


# plot_flight_timeseries_with_seed_and_penetration_vlines(
#     wind_df, "lwc [g/m^3]", seeds, pens
# )


plot_barplot_penetrations(
    in_cloud,
    title=f"RCSP aircraft: {aircraft}, mission: {date} ({start_str} - {end_str} UTC)",
    filename=f"{CS_BARPLOTS}/pen-categories/{aircraft}_{dt_str}.png",
)

plot_barplot_seeds(
    seeds,
    title=f"RCSP aircraft: {aircraft}, mission: {date} ({start_str} - {end_str} UTC)",
    filename=f"{CS_BARPLOTS}/seed-categories/{aircraft}_{dt_str}.png",
)


penetration_durations = (
    in_cloud.groupby("in_cloud_id")
    .agg(
        duration_seconds=("flare_fired", "size"),  # counts rows = seconds
        flare_fired=("flare_fired", "any"),  # True if any flare fired
    )
    .reset_index()
)


plot_barplot_penetration_durations(
    penetration_durations,
    title=f"RCSP aircraft: {aircraft}, mission: {date} ({start_str} - {end_str} UTC)",
    filename=f"{CS_BARPLOTS}/seed-durations/{aircraft}_{dt_str}.png",
)


summary_df = calc_summary(wind_df, wind_file).T
summary_df.to_csv(
    f"{CS_TABLES}/{aircraft}_{dt_str}_summary.csv", header=False
)
seeds[["lat [deg]", "lon [deg]", "gps_alt [m]"]].to_csv(
    f"{CS_TABLES}/{aircraft}_{dt_str}_seed_locations.csv"
)

if len(seeds) < 1:
    raise EmptyDataError(f"No seed events for {date}, {aircraft}")


# plot_confusion_matrix_seed_or_pen(
#     in_cloud_or_flare_fired,
#     title=f"{aircraft}, {date_hour_min}",
#     filename=f"plots/case-study/confusion-matrix/{aircraft}_{dt_str}.png",
# )

flare_cloud_ids = in_cloud.groupby("in_cloud_id")["flare_fired"].any()
flare_cloud_ids = flare_cloud_ids[flare_cloud_ids].index

pens_with_flares = in_cloud[
    in_cloud["in_cloud_id"].isin(flare_cloud_ids)
].copy()


flares_in_cloud_extent = get_map_extent(flares_in_cloud, offset=0.05)
plot_flight_track_with_pens_and_seeds(
    wind_df,
    flares_in_cloud,
    pens_with_flares,
    extent=flares_in_cloud_extent,
    radar_label_offset=0.01,
    title=f"RCSP aircraft: {aircraft}, flight track: {date} \n ({start_str} - {end_str} UTC)",
    filename=f"{CS_MAPS}/pens-seeds/{aircraft}_{dt_str}.png",
)

plot_flight_multi_timeseries_with_vlines(
    wind_df,
    seeds,
    penetrations=in_cloud,
    title=f"RCSP aircraft: {aircraft}, CWIP measurements: {date} ({start_str} - {end_str} UTC)",
    filename=f"{CS_TIMESERIES}/all-flight/{aircraft}_{dt_str}.png",
)


cols = [
    "lwc [g/m^3]",
    "rh [%]",
    "temp_amb [C]",
    "wind_w [m/s]",
    "ss_total [%]",
]

for pen_id, group in wind_df.groupby("cloud_id"):
    half_window = WINDOW_SEC // 2
    start_time = group.index.min() - pd.Timedelta(seconds=half_window)
    end_time = group.index.max() + pd.Timedelta(seconds=half_window)
    pen_window_df = wind_df[start_time:end_time]
    if not pen_window_df["flare_fired"].any():
        print(f"No flare fired in {aircraft}_{dt_str}_p{pen_id}")
        continue
    if len(pen_window_df) < WINDOW_SEC + 3:
        print(f"Penetration < 3 in {aircraft}_{dt_str}_p{pen_id}")
        continue
    plot_time_window_multi_timeseries_with_pens_and_vlines(
        pen_window_df,
        cols,
        title=f"RCSP aircraft: {aircraft}, CWIP measurements: {date} ({start_str} - {end_str} UTC, \n Cloud penetration: {pen_id}",
        filename=f"{CS_TIMESERIES}/each-penetration-window/{aircraft}/{aircraft}_{dt_str}_p{pen_id}.png",
    )


win_td = pd.Timedelta(seconds=WINDOW_SEC)
seed_windows_list = select_time_windows(wind_df, seeds, win_td)
pen_windows_list = select_time_windows(wind_df, in_cloud, win_td)

seed_windows_df = time_windows_to_df(seed_windows_list)
pen_windows_df = time_windows_to_df(pen_windows_list)

# seed_in_pen = pen_windows_df.loc[seeds.index]
seed_in_pen = pd.merge(seeds, pen_windows_df, how="inner", on="datetime")
pens_with_seed_count = seed_in_pen["window_count"].value_counts().sort_index()
windows_description = describe_time_windows(
    seeds, in_cloud, pens_with_seed_count
)


# plot_bar_pens_per_window(pens_with_seed_count)


# Plot each event
# plot_pen_window_timeseries(seed_windows_list, aircraft, dt_str, "seed-event")
# plot_seed_window_timeseries(pen_windows_list, aircraft, dt_str, "penetration")


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
        f"{CS_BOXPLOTS}/by-seed-event/{aircraft}/{aircraft}_{dt_str}.png"
    ),
    title=f"RCSP aircraft: {aircraft}, CWIP measurements: {date} ({start_str} - {end_str} UTC) \n  time window: {WINDOW_SEC} s",
)


plot_flight_boxplots_by_event(
    pen_windows_df,
    "lwc [g/m^3]",
    start_ts,
    aircraft,
    window_seconds=WINDOW_SEC,
    filename=(
        f"{CS_BOXPLOTS}/by-penetration/{aircraft}/{aircraft}_{dt_str}.png"
    ),
    xlabel="Cloud penetrations",
    title=f"RCSP aircraft: {aircraft}, CWIP measurements: {date} ({start_str} - {end_str} UTC) \n  time window: {WINDOW_SEC} s",
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
    "wind_w [m/s]",
]
for col in cols:
    var_tag = col.split(" ")[0]

    plot_boxplot_by_relative_time(
        seed_windows_rel_df,
        col,
        title=f"RCSP aircraft: {aircraft}, CWIP measurements: {date} ({start_str} - {end_str} UTC)",
        filename=(
            f"{CS_BOXPLOTS}/by-seed-relative-time/{aircraft}/{aircraft}_{dt_str}_{var_tag}.png"
        ),
    )

    plot_boxplot_by_relative_time(
        pen_windows_rel_df,
        col,
        title=f"RCSP aircraft: {aircraft}, CWIP measurements: {date} ({start_str} - {end_str} UTC)",
        filename=(
            f"{CS_BOXPLOTS}/by-penetration-relative-time/{aircraft}/{aircraft}_{dt_str}_{var_tag}.png"
        ),
        xlabel="Time relative to cloud penetrations (s)",
    )

plot_boxplot_pens_seeds(
    in_cloud,
    seeds,
    dt_str,
    aircraft,
    title=f"RCSP aircraft: {aircraft}, CWIP measurements: \n {date} ({start_str} - {end_str} UTC)",
    filename=f"{CS_BOXPLOTS}/pen-vs-seed/{aircraft}/{aircraft}_{dt_str}_lwc.png",
)
