import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from utils.plotting import MEDIUM_SIZE, LARGE_SIZE, col_to_label, savefig
from utils.utils import get_index_middle
from utils.time_window import to_relative_time_index
from plotting_time_window import plot_multiple_timeseries


def plot_confusion_matrix_seed_or_pen(df, filename="", title=""):
    cross_tab = pd.crosstab(df["flare_fired"], df["is_in_cloud"])
    plt.rc("font", size=MEDIUM_SIZE)
    sns.heatmap(
        cross_tab,
        annot=True,
        cmap="Blues",
        cbar=False,
        linewidths=1,
        linecolor="k",
    )
    plt.xlabel("In cloud")
    plt.ylabel("Flare fired")
    plt.title(title)
    plt.tight_layout()
    savefig(filename)
    plt.show()


def plot_barplot_penetrations(df, title="", filename=""):
    pen_summary = df.groupby("in_cloud_id")["flare_fired"].any()
    pens_total = len(pen_summary)
    pens_with_flares = pen_summary.sum()
    pens_no_flare = pens_total - pens_with_flares

    counts_df = pd.DataFrame(
        [
            ("Total", pens_total),
            ("With flares", pens_with_flares),
            ("No flare", pens_no_flare),
        ],
        columns=["Category", "Count"],
    )

    counts_df = counts_df.sort_values("Count", ascending=False)
    plt.rc("font", size=MEDIUM_SIZE)
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(counts_df, y="Count", x="Category", edgecolor="k")
    ax.bar_label(ax.containers[0])
    ax.set_xlabel("Cloud penetrations")
    plt.title(title)
    plt.tight_layout()
    savefig(filename)
    plt.show()


def plot_barplot_seeds(df, title="", filename=""):
    total_flares = len(df)
    flares_in_cloud = df["is_in_cloud"].sum()
    flares_not_in_cloud = (~df["is_in_cloud"]).sum()
    counts_df = pd.DataFrame(
        [
            ("Total", total_flares),
            ("In cloud", flares_in_cloud),
            ("Out of cloud", flares_not_in_cloud),
        ],
        columns=["Category", "Count"],
    )
    # counts_df.sort_values("Count", ascending=False)
    plt.rc("font", size=MEDIUM_SIZE)
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(counts_df, y="Count", x="Category", edgecolor="k")
    ax.bar_label(ax.containers[0])
    ax.set_xlabel("Flares fired")
    plt.title(title)
    plt.tight_layout()
    savefig(filename)
    plt.show()


def plot_barplot_penetration_durations(df, title="", filename=""):
    fig_width = max(8, len(df) * 0.35)  # 0.5 inches per bar, minimum width 8
    plt.figure(figsize=(fig_width, 6))
    plt.rc("font", size=MEDIUM_SIZE)
    sns.barplot(
        data=df,
        x="in_cloud_id",
        y="duration_seconds",
        hue="flare_fired",
        edgecolor="k",
    )
    plt.grid(axis="y")
    plt.locator_params(axis="y", nbins=min(len(df), 20))
    plt.xlabel("Cloud penetration ID")
    plt.ylabel("Duration (s)")
    plt.title(title)
    plt.legend(title="Flares fired")
    savefig(filename)
    plt.show()


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
    savefig(filename)
    plt.show()


def plot_flight_multi_timeseries_with_seed_and_penetration_vlines(
    df, col, seed_locations, penetrations, filename="", title=""
):
    plt.rc("font", size=MEDIUM_SIZE)

    fig, ax = plt.subplots(figsize=(18, 4))
    add_vlines(ax, penetrations, color="green", label="Penetrations")
    add_vlines(ax, seed_locations, color="orange", label="Seed events", ls="--")
    (line,) = ax.plot(df[col], label=col)
    # ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_ylabel(col)
    ax.set_xlabel("Time-UTC")
    plt.title(title)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    savefig(filename)
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
        showfliers=False,
        legend=False,
    )
    plt.title(title)
    plt.xlabel("")
    plt.ylabel(col_to_label(col))
    plt.tight_layout()
    savefig(filename)
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


def plot_time_window_multi_timeseries_with_pens_and_vlines(
    df, columns, xlabel="Time, UTC", title="", filename=""
):
    n = len(columns)
    cloud_ids = df["cloud_id"].dropna().unique()
    flares_in_window = df.loc[df["flare_fired"] == True]
    plt.rc("font", size=MEDIUM_SIZE)
    fig, axes = plt.subplots(n, 1, figsize=(12, 2 * n), sharex=True)
    if n == 1:
        axes = [axes]
    for ax, col in zip(axes, columns):
        ax.plot(df.index, df[col], color="grey", label="Out of cloud")
        for cloud_id in cloud_ids:
            cloud_mask = df["cloud_id"] == cloud_id
            ax.plot(
                df.index[cloud_mask],
                df[col][cloud_mask],
                marker="o",
                linewidth=4,
                label=f"Cloud penetration {int(cloud_id)}",
            )
        ax.set_ylabel(col_to_label(col))
        axes[-1].set_xlabel(xlabel)
        ax.grid()
        add_vlines(ax, flares_in_window, label="Seed event", color="red")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.03)
    )
    fig.suptitle(title, fontsize=LARGE_SIZE)
    plt.tight_layout()
    savefig(filename)
    plt.show()
