import seaborn as sns
import matplotlib.pyplot as plt
from utils_plotting import MEDIUM_SIZE, col_to_label, savefig


def plot_multiple_timeseries(df, columns, xlabel="", filename="", title=""):
    n = len(columns)
    fig, axes = plt.subplots(n, 1, figsize=(10, 2 * n), sharex=True)
    plt.rc("font", size=MEDIUM_SIZE)
    if n == 1:
        axes = [axes]
    for ax, col in zip(axes, columns):
        ax.plot(df.index, df[col])
        ax.set_ylabel(col_to_label(col))
        ax.axvline(x=0, color="red", linestyle="--")
    axes[-1].set_xlabel(xlabel)
    plt.suptitle(title)
    plt.tight_layout()
    savefig(filename)
    plt.show()


def plot_flight_boxplots_by_event(
    df,
    col,
    start_timestamp,
    aircraft,
    window_seconds,
    filename="",
    xlabel="Seed events",
    title="",
):
    """Plots a single plot for all flight
    where each event is represented by a boxplot"""
    time_windows_clean = df.dropna(subset=[col])
    num_time_windows = max(df["window_count"])
    if num_time_windows > 0:
        width = max(6, num_time_windows * 0.4)  # scales with number of boxes
        height = 5
        plt.figure(figsize=(width, height))
        plt.rc("font", size=MEDIUM_SIZE)
        plt.xlabel(xlabel)
        plt.ylabel(col_to_label(col))
        plt.title(title)
        sns.boxplot(
            data=time_windows_clean, x="window_count", y=col, showfliers=False
        )
        savefig(filename)
        plt.show()
    else:
        print(f"No values to plot for {aircraft}, {start_timestamp}")


def plot_barplot_by_relative_time(
    df, col, title="", filename="", xlabel="Time relative to seed event (s)"
):
    plt.figure(figsize=(12, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    sns.barplot(
        data=df,
        x="relative_time",
        y=col,
        # estimator="max",
        # showfliers=False,
    )
    plt.xlabel(xlabel)
    plt.ylabel(col_to_label(col))
    plt.title(title)
    plt.suptitle("")
    savefig(filename)
    plt.show()


def plot_boxplot_by_relative_time(
    df,
    col,
    title="",
    filename="",
    window_seconds=8,
    xlabel="Time relative to seed event (s)",
):
    df_rel = df.copy()

    time_min = -window_seconds // 2
    time_max = window_seconds // 2

    # Filter by index (relative_time)
    df_rel = df_rel[(df_rel.index >= time_min) & (df_rel.index <= time_max)]

    # Drop bins with no data
    valid_bins = df_rel.groupby(df_rel.index)[col].apply(
        lambda x: x.notna().any()
    )
    df_rel = df_rel[df_rel.index.isin(valid_bins[valid_bins].index)]
    df_rel = df_rel.reset_index()

    plt.figure(figsize=(12, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    sns.boxplot(data=df_rel, x="relative_time", y=col, showfliers=False)
    plt.xlabel(xlabel)
    plt.ylabel(col_to_label(col))
    plt.title(title)
    savefig(filename)
    plt.show()


def plot_flight_timeseries_lwc_diff(df, threshold):
    plt.figure(figsize=(12, 4))
    df["lwc [g/m^3]"].plot(label="LWC")
    df["lwc [g/m^3]"].diff().plot(label="LWC diff", alpha=0.8)
    plt.axhline(threshold, color="red", linestyle="--", label="threshold")
    plt.legend()
    plt.show()


def plot_flight_timeseries_lwc_diff_over_threshold(df, threshold):
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
