import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import os
from utils_plotting import MEDIUM_SIZE, col_to_label
from utils import get_index_middle
from utils_time_window import to_relative_time_index
from plotting_time_window import plot_multiple_timeseries


def add_vlines(ax, line_locations_df, color="orange", label="", ls="-"):
    if len(line_locations_df) > 0:
        vlines = []
        for event in line_locations_df.index:
            vlines.append(ax.axvline(event, color=color, alpha=0.7, ls=ls))
        vlines[0].set_label(f"{label}: {len(line_locations_df)}")


def plot_flight_timeseries_with_seed_and_penetration_vlines(
    df, col, seed_locations, penetrations, filename=""
):
    date = df.index[0].date()
    aircraft = df.iloc[:, -1].values[0]
    plt.rc("font", size=MEDIUM_SIZE)

    fig, ax = plt.subplots(figsize=(18, 4))
    add_vlines(ax, penetrations, color="green", label="Penetrations")
    add_vlines(ax, seed_locations, color="orange", label="Seed events", ls="--")
    (line,) = ax.plot(df[col], label=col)
    # ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_ylabel(col)
    ax.set_xlabel("Time-UTC")
    plt.title(f"{date}, {aircraft}")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)
    plt.show()


def plot_bar_pens_per_window(seed_in_pen):
    plt.rc("font", size=MEDIUM_SIZE)
    plt.figure(figsize=(16, 6))
    seed_in_pen.plot(kind="bar", edgecolor="black")
    plt.title("Number of Penetrations per Window")
    plt.xlabel("Cloud penetration")
    plt.ylabel("Number of Penetrations")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_boxplot_pens_seeds(
    pens, seeds, dt_str, aircraft, col="lwc [g/m^3]", title="", filename=""
):
    df_seeds = seeds[[col]].assign(group="Seed events")
    df_pens = pens[[col]].assign(group="Cloud penetrations")
    combined = pd.concat([df_seeds, df_pens])
    plt.figure()
    sns.boxplot(
        data=combined,
        x="group",
        y=col,
        hue="group",
        width=0.4,
        # palette="Set2",
        legend=False,
    )
    plt.title(title)
    plt.xlabel("")
    plt.ylabel(col_to_label(col))
    plt.tight_layout()
    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename, bbox_inches="tight")
    plt.show()


def plot_pen_window_timeseries(
    windows_list, aircraft, dt_str, event_type="penetration"
):
    """Plot multi-timeseries for each cloud penetration time window"""
    initials = event_type[0]
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
        # seed_in_pen = pd.merge(seeds, windows_list[1], how="inner", on="datetime")
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


def plot_seed_window_timeseries(
    windows_list, aircraft, dt_str, event_type="seed"
):
    """Plot multi-timeseries for each seed event time window"""
    initials = event_type[0]
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
        # seed_in_pen = pd.merge(seeds, windows_list[1], how="inner", on="datetime")
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
