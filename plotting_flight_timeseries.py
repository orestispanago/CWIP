import matplotlib.pyplot as plt
import matplotlib.dates as mdates


SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


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


def add_seed_lines(
    ax, seed_locations, label_first=False, label="seed-a", color="orange"
):
    for i, event in enumerate(seed_locations.index):
        line = ax.axvline(event, color=color)
        if label_first and i == 0:
            line.set_label(label)


def plot_flight_multi_timeseries_with_seed_vlines(df, seed_locations):

    seed_a_events = df[df["seed-a [cnt]"].diff() > 0]
    seed_b_events = df[df["seed-b [cnt]"].diff() > 0]

    plt.rc("font", size=MEDIUM_SIZE)
    fig, axes = plt.subplots(3, 1, figsize=(18, 9), sharex=True)

    if len(seed_a_events) > 0:
        add_seed_lines(
            axes[0],
            seed_a_events,
            label_first=True,
            label="seed-a",
            color="tab:green",
        )
        axes[0].legend(loc="upper left", bbox_to_anchor=(1.05, 1))
        for ax in axes[1:]:
            add_seed_lines(ax, seed_a_events, label="seed-a", color="tab:green")

    if len(seed_b_events) > 0:
        add_seed_lines(
            axes[0],
            seed_b_events,
            label_first=True,
            label="seed-b",
            color="tab:orange",
        )
        axes[0].legend(loc="upper left", bbox_to_anchor=(1.05, 1))
        for ax in axes[1:]:
            add_seed_lines(
                ax, seed_b_events, label="seed-b", color="tab:orange"
            )

    ax1 = axes[0]
    lwc_color = "tab:blue"
    ax1.plot(df.index, df["lwc [g/m^3]"], color=lwc_color)
    ax1.set_ylabel("lwc [g/m^3]", color=lwc_color)

    ax1.tick_params(axis="y", labelcolor=lwc_color)

    ax2 = axes[1]
    alt_color = "tab:blue"
    alt_km = df["gps_alt [m]"] / 1000
    ax2.plot(df.index, alt_km, color=alt_color)
    ax2.tick_params(axis="y", labelcolor=alt_color)
    ax2.set_ylabel("gps_alt [km]", color=alt_color)

    ax3 = ax2.twinx()
    temp_color = "tab:red"
    # ax3.set_ylim([-17, 45])
    ax3.axhline(-15, color=temp_color, linestyle="--")
    ax3.axhline(-10, color=temp_color, linestyle="--")
    ax3.axhline(-5, color=temp_color, linestyle="--")
    ax3.tick_params(axis="y", labelcolor=temp_color)
    ax3.plot(df.index, df["temp_amb [C]"], color=temp_color)
    ax3.set_ylabel("temp_amb [C]", color=temp_color)
    ax3.invert_yaxis()

    ax4 = ax1.twinx()
    rh_color = "tab:red"
    ax4.plot(df.index, df["rh [%]"], color=rh_color)
    ax4.tick_params(axis="y", labelcolor=rh_color)
    ax4.set_ylabel("rh [%]", color=rh_color)

    ax5 = axes[2]
    wind_color = "tab:blue"
    ax5.plot(df.index, df["wind_w [m/s]"], color=wind_color)
    ax5.tick_params(axis="y", labelcolor=wind_color)
    ax5.set_ylabel("wind_w [m/s] (+up)", color=wind_color)

    ax5.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax5.set_xlabel("Time-UTC")

    aircraft = df.iloc[:, -1].dropna().values[0]
    start_timestamp = df.index[0]
    date_time = start_timestamp.strftime("%Y%m%d_%H%M%S")
    fig.suptitle(f"{start_timestamp}, {aircraft}")
    plt.tight_layout()
    plt.savefig(f"plots/timeseries/{date_time}_{aircraft}.png")
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
