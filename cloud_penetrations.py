import pandas as pd
import glob
import matplotlib.pyplot as plt
from readers import read_wind_csv
from plotting import *
import seaborn as sns
import os

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


def to_relative_time_index(df):
    """Returns a new DataFrame with the index converted to relative seconds
    from the center timestamp, corresponding to the seed event."""
    df_rel = df.copy()
    center_time = df_rel.index[len(df_rel) // 2]
    df_rel["relative_time"] = (
        (df_rel.index - center_time).total_seconds().astype(int)
    )
    df_rel = df_rel.set_index("relative_time")
    return df_rel


def plot_flight_boxplot_per_seed_event(
    df, col, start_timestamp, aircraft, filename=""
):
    time_windows_clean = df.dropna(subset=[col])
    num_time_windows = max(df["window_count"])
    if num_time_windows > 0:
        width = max(6, num_time_windows * 0.4)  # scales with number of boxes
        height = 5
        plt.figure(figsize=(width, height))
        plt.rc("font", size=MEDIUM_SIZE)
        plt.xlabel("Seed events")
        plt.ylabel(col)
        plt.title(f"{start_timestamp}, time window: {window_seconds} s")
        sns.boxplot(
            data=time_windows_clean, x="window_count", y=col, showfliers=False
        )
        if filename:
            plt.savefig(filename)
        plt.show()
    else:
        print(f"No values to plot for {start_timestamp}, {aircraft}")


def plot_barplot_by_relative_time(df, col, title="", filename=""):
    plt.figure(figsize=(12, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    sns.barplot(
        data=df,
        x="relative_time",
        y=col,
        # estimator="max",
        # showfliers=False,
    )
    plt.xlabel("Time relative to seed event (s)")
    plt.ylabel(col)
    plt.title(title)
    plt.suptitle("")
    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)
    plt.show()


def plot_boxplot_by_relative_time(df, col, title="", filename=""):
    df_rel = df.copy()
    # df_rel["relative_time_binned"] = df_rel["relative_time"].round().astype(int)
    # Drop bins with no data
    valid_bins = df_rel.groupby("relative_time")[col].apply(
        lambda x: x.notna().any()
    )
    df_rel = df_rel[df_rel["relative_time"].isin(valid_bins[valid_bins].index)]

    plt.figure(figsize=(12, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    sns.boxplot(
        data=df_rel,
        x="relative_time",
        y=col,
        showfliers=False,
    )
    plt.xlabel("Time relative to seed event (s)")
    plt.ylabel(col)
    plt.title(title)
    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)
    plt.show()


def plot_flight_timeseries_lwc_diff(df, threshold):
    plt.figure(figsize=(12, 4))
    df["lwc [g/m^3]"].plot(label="LWC")
    df["lwc [g/m^3]"].diff().plot(label="LWC diff", alpha=0.8)
    plt.axhline(threshold, color="red", linestyle="--", label="threshold")
    plt.title(count)
    plt.legend()
    plt.show()


def plot_flight_timeseries_lwc_diff_over_threshold(df):
    diff_over_threshold = df[df["diff"] > threshold]
    if len(diff_over_threshold) > 0:
        plt.figure(figsize=(12, 4))
        df["lwc [g/m^3]"].plot(label="LWC")
        diff_over_threshold["diff"].plot(label="diff > threshold", style=".")
        plt.axhline(threshold, color="red", linestyle="--", label="threshold")
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.show()
    else:
        print(f"No LWC > {threshold} to plot for {df.index[0]}")


def select_seed_locations(df):
    return df[(df["seed-a [cnt]"].diff() > 0) | (df["seed-b [cnt]"].diff() > 0)]


def select_time_windows(df, center_times, window_timedelta):
    time_windows = []
    for count, time in enumerate(center_times.index):
        start = time - window_timedelta / 2
        end = time + window_timedelta / 2
        time_window = df[start:end].copy()
        time_window["window_count"] = count
        if not time_window.empty:
            time_windows.append(time_window)
    return time_windows


def time_windows_to_df(time_windows):
    time_windows_list = []
    for count, time_window in enumerate(time_windows):
        time_window_c = time_window.copy()
        time_windows_list.append(time_window_c)
    return pd.concat(time_windows_list)


wind_files = glob.glob("*/*/*/*/*wind.csv")
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

    # plot_flight_timeseries_lwc_diff_over_threshold(resampled)

    if len(seed_locations) > 0:
        seed_event_windows = select_time_windows(
            wind, seed_locations, window_timedelta
        )
        seed_event_windows_df = time_windows_to_df(seed_event_windows)
        plot_flight_boxplot_per_seed_event(
            seed_event_windows_df,
            "lwc [g/m^3]",
            start_timestamp,
            aircraft,
            filename=f"plots/boxplots/per-seed-event/{date_time}_{aircraft}.png",
        )

        # seed_event_example = to_relative_time_index(seed_event_windows[0])
        # plot_multiple_timeseries(seed_event_example, ["lwc [g/m^3]", "rh [%]","temp_amb [C]","wind_w [m/s]", "ss_total [%]"])

        seed_event_windows_rel = [
            to_relative_time_index(df) for df in seed_event_windows
        ]
        seed_event_windows_df_rel = pd.concat(
            seed_event_windows_rel
        ).reset_index()

        all_seed_event_windows_rel_list.append(seed_event_windows_df_rel)

        plot_boxplot_by_relative_time(
            seed_event_windows_df_rel,
            "lwc [g/m^3]",
            title=f"{start_timestamp}, {aircraft}",
            filename=f"plots/boxplots/by-relative-time/{date_time}_{aircraft}_lwc.png",
        )

    # else:
    #     print(f"No seed events for {start_timestamp}, {aircraft}")
all_seed_event_windows_rel_df = pd.concat(
    all_seed_event_windows_rel_list
).reset_index()
plot_boxplot_by_relative_time(
    all_seed_event_windows_rel_df,
    "lwc [g/m^3]",
    filename="plots/boxplots/all-flights/lwc.png",
)
# plot_boxplot_by_relative_time(all_seed_event_windows_rel_df, "rh [%]", filename="plots/boxplots/all-flights/rh.png")
# plot_boxplot_by_relative_time(all_seed_event_windows_rel_df, "wind_w [m/s]", filename="plots/boxplots/all-flights/wind_w.png")
# plot_boxplot_by_relative_time(all_seed_event_windows_rel_df, "ss_total [%]", filename="plots/boxplots/all-flights/ss_total.png")
