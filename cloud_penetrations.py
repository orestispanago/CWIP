import pandas as pd
import glob
import matplotlib.pyplot as plt
from readers import read_wind_csv
from plotting import *
import matplotlib.dates as mdates
import seaborn as sns


MEDIUM_SIZE = 14


def resample_1s(df):
    numeric_cols = df.select_dtypes(include="number").columns
    string_cols = df.select_dtypes(exclude="number").columns
    # Resample numeric and string parts separately
    numeric_resampled = df[numeric_cols].resample("1s").mean()
    string_resampled = df[string_cols].resample("1s").first()  # or .last()
    # Combine them back
    return pd.concat([numeric_resampled, string_resampled], axis=1)


def plot_multiple_timeseries(df, columns, xlabel=""):
    n = len(columns)
    fig, axes = plt.subplots(n, 1, figsize=(10, 2 * n), sharex=True)
    plt.rc("font", size=MEDIUM_SIZE)
    if n == 1:
        axes = [axes]
    for ax, col in zip(axes, columns):
        ax.plot(df.index, df[col])
        ax.set_ylabel(col)
        ax.axvline(x=0, color="red", linestyle="--")
    axes[-1].set_xlabel(xlabel)
    plt.tight_layout()
    plt.show()


def convert_to_relative_time(df):
    """Converts index of time window dataframe to relative index (integer)
    around center time"""
    df_rel = df.copy()
    center_time = df_rel.index[len(df) // 2]
    df_rel["relative_time"] = (df_rel.index - center_time).total_seconds()
    df_rel = df_rel.set_index("relative_time")
    return df_rel


def plot_boxplot_per_seed_events(lwc_values):
    plt.figure(figsize=(14, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    plt.boxplot(lwc_values)
    plt.ylabel("lwc [g/m^3]")
    timestamp = resampled.index[0]
    plt.title(f"{timestamp}, time window: {window_seconds} s")
    plt.show()


def plot_boxplot_by_relative_time(seed_event_windows):
    relative_windows = [
        convert_to_relative_time(df) for df in seed_event_windows
    ]
    relative_lwc_dfs = [df[["lwc [g/m^3]"]] for df in relative_windows]
    combined_df = pd.concat(relative_lwc_dfs)
    combined_df_reset = combined_df.reset_index()
    plt.figure(figsize=(12, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    sns.boxplot(
        data=combined_df_reset,
        x="relative_time",
        y="lwc [g/m^3]",
        # showfliers=False,
    )
    plt.xlabel("Time relative to seed event (s)")
    plt.ylabel("lwc [g/m^3]")
    plt.title("")
    plt.suptitle("")
    plt.show()


wind_files = glob.glob("*/*/*/*/*wind.csv")

lwc_diff_over_threshold_list = []
seed_locations_list = []
for wind_file in wind_files[2:3]:

    wind = read_wind_csv(wind_file)

    seed_locations = wind[
        (wind["seed-a [cnt]"].diff() > 0) | (wind["seed-b [cnt]"].diff() > 0)
    ]

    resampled = resample_1s(wind)
    seed_locations_list.append(seed_locations)

    threshold = 0.3
    window_seconds = 8
    window_mid = int(window_seconds / 2)
    window_timedelta = pd.Timedelta(seconds=window_seconds)

    relative_times = list(range(-window_mid, window_mid + 1))
    # plt.figure(figsize=(12, 4))
    # resampled["lwc [g/m^3]"].plot(label="LWC")
    # resampled["lwc [g/m^3]"].diff().plot(label="LWC diff", alpha=0.8)
    # plt.axhline(threshold, color="red", linestyle="--", label="threshold")
    # plt.legend()
    # plt.show()

    resampled["diff"] = resampled["lwc [g/m^3]"].diff()
    diff_over_threshold = resampled[resampled["diff"] > threshold]

    lwc_diff_over_threshold_list.append(diff_over_threshold)

    # plt.figure(figsize=(12, 4))
    # resampled["lwc [g/m^3]"].plot(label="LWC")
    # diff_over_threshold["diff"].plot(label="diff > threshold", style=".")
    # plt.axhline(threshold, color="red", linestyle="--", label="threshold")
    # plt.legend()
    # plt.show()

    # event_times = diff_over_threshold.index

    # plt.figure(figsize=(12, 4))
    # diff_over_threshold["diff"].plot(label="diff > threshold", style=".")
    # plt.axhline(threshold, color="red", linestyle="--", label="threshold")

    seed_event_windows = []
    time_window_lwc_values = []
    for time in seed_locations.index:
        start = time - window_timedelta / 2
        end = time + window_timedelta / 2
        time_window = resampled[start:end]
        seed_event_windows.append(time_window)
        time_window_lwc_values.append(time_window["lwc [g/m^3]"].values)

    plot_boxplot_per_seed_events(time_window_lwc_values)

    seed_event_windows_rel = convert_to_relative_time(seed_event_windows[4])
    plot_multiple_timeseries(
        seed_event_windows_rel,
        [
            "lwc [g/m^3]",
            "rh [%]",
            "temp_amb [C]",
            "wind_w [m/s]",
            "ss_total [%]",
        ],
    )

    plot_boxplot_by_relative_time(seed_event_windows)


# all_lwc_diff_over_threshold = pd.concat(lwc_diff_over_threshold_list)
# all_seed_locations = pd.concat(seed_locations_list)

# plot_scatter(all_seed_locations, "lwc [g/m^3]", "ss_total [%]", title="Seed locations")
# plot_scatter(all_lwc_diff_over_threshold, "lwc [g/m^3]", "ss_total [%]", title=f"LWC diff > {threshold}")

# plot_scatter(all_lwc_diff_over_threshold, "diff", "ss_total [%]", title=f"LWC diff > {threshold}")
