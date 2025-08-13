import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.plotting import MEDIUM_SIZE, col_to_label, savefig


def plot_flight_timeseries_with_seed_vlines(df, col, seed_locations):
    date = df.index[0].date()
    aircraft = df.iloc[:, -1].values[0]

    fig, ax = plt.subplots(figsize=(10, 4))
    if len(seed_locations) > 0:
        vlines = []
        for event in seed_locations.index:
            vlines.append(ax.axvline(event, color="orange"))
        vlines[0].set_label("Seed")
    (line,) = ax.plot(df[col], label=aircraft)
    # ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_ylabel(col)
    ax.set_xlabel("Time-UTC")
    plt.title(f"{date}, {aircraft}")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.show()


def add_vlines(ax, lines_df, label_first=False, label="seed-a", color="orange"):
    for i, event in enumerate(lines_df.index):
        line = ax.axvline(event, color=color)
        if label_first and i == 0:
            line.set_label(label)


def plot_flight_multi_timeseries_with_vlines(
    df, seed_locations, penetrations="", filename=""
):

    seed_a_events = df[df["seed-a [cnt]"].diff() > 0]
    seed_b_events = df[df["seed-b [cnt]"].diff() > 0]

    plt.rc("font", size=MEDIUM_SIZE)
    fig, axes = plt.subplots(3, 1, figsize=(18, 9), sharex=True)
    if len(penetrations) > 0:
        add_vlines(
            axes[0],
            penetrations,
            label_first=True,
            label="In cloud",
            color="tab:orange",
        )
        axes[0].legend(loc="upper left", bbox_to_anchor=(1.05, 1))
        for ax in axes[1:]:
            add_vlines(ax, penetrations, label="In cloud", color="tab:orange")

    if len(seed_a_events) > 0:
        add_vlines(
            axes[0],
            seed_a_events,
            label_first=True,
            label="seed-a",
            color="magenta",
        )
        axes[0].legend(loc="upper left", bbox_to_anchor=(1.05, 1))
        for ax in axes[1:]:
            add_vlines(ax, seed_a_events, label="seed-a", color="magenta")

    if len(seed_b_events) > 0:
        add_vlines(
            axes[0],
            seed_b_events,
            label_first=True,
            label="seed-b",
            color="tab:green",
        )
        axes[0].legend(loc="upper left", bbox_to_anchor=(1.05, 1))
        for ax in axes[1:]:
            add_vlines(ax, seed_b_events, label="seed-b", color="tab:green")

    ax1 = axes[0]
    col = "lwc [g/m^3]"
    lwc_color = "tab:blue"
    ax1.plot(df.index, df[col], color=lwc_color)
    ax1.set_ylabel(col_to_label(col), color=lwc_color)

    ax1.tick_params(axis="y", labelcolor=lwc_color)

    ax2 = axes[1]
    col = "gps_alt [m]"
    alt_color = "tab:blue"
    alt_km = df[col] / 1000
    ax2.plot(df.index, alt_km, color=alt_color)
    ax2.tick_params(axis="y", labelcolor=alt_color)
    ax2.set_ylabel("Altitude (km)", color=alt_color)

    ax3 = ax2.twinx()
    col = "temp_amb [C]"
    temp_color = "tab:red"
    # ax3.set_ylim([-17, 45])
    ax3.axhline(-15, color=temp_color, linestyle="--")
    ax3.axhline(-10, color=temp_color, linestyle="--")
    ax3.axhline(-5, color=temp_color, linestyle="--")
    ax3.tick_params(axis="y", labelcolor=temp_color)
    ax3.plot(df.index, df[col], color=temp_color)
    ax3.set_ylabel(col_to_label(col), color=temp_color)
    ax3.invert_yaxis()

    ax4 = ax1.twinx()
    col = "rh [%]"
    rh_color = "tab:red"
    ax4.plot(df.index, df[col], color=rh_color)
    ax4.tick_params(axis="y", labelcolor=rh_color)
    ax4.set_ylabel(col_to_label(col), color=rh_color)

    ax5 = axes[2]
    col = "wind_w [m/s]"
    wind_color = "tab:blue"
    ax5.plot(df.index, df[col], color=wind_color)
    ax5.tick_params(axis="y", labelcolor=wind_color)
    ax5.set_ylabel(col_to_label(col), color=wind_color)

    ax5.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax5.set_xlabel("Time-UTC")

    aircraft = df["aircraft"].values[0]
    start_timestamp = df.index[0]
    fig.suptitle(f"{start_timestamp}, {aircraft}")
    plt.tight_layout()
    savefig(filename)
    plt.show()


def plot_day_timeseries_with_seed_vlines(df, col):
    last_column = df.iloc[:, -1]  # last column is named aircraft
    seed_by_plane = [group for _, group in df.groupby(last_column)]

    fig, ax = plt.subplots(figsize=(10, 4))
    for plane in seed_by_plane:
        seed_locations = plane[
            (plane["seed-a [cnt]"].diff() > 0)
            | (plane["seed-b [cnt]"].diff() > 0)
        ]
        aircraft = plane.iloc[:, -1].values[0]
        (line,) = ax.plot(plane[col], label=aircraft)
        if len(seed_locations) > 0:
            line_color = line.get_color()
            vlines = []
            for event in seed_locations.index:
                vlines.append(
                    ax.axvline(
                        event, linestyle="--", color=line_color, linewidth=0.5
                    )
                )
            vlines[0].set_label(f"Seed: {aircraft}")
    ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_ylabel(col)
    ax.set_xlabel("Time-UTC")
    date_time = df.index[0].strftime("%Y%m%d_%H%M%S")
    plt.title(df.index[0].date())
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.show()
