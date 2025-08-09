import matplotlib.pyplot as plt
import matplotlib.dates as mdates


SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


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
        plt.savefig(filename)
    plt.show()
