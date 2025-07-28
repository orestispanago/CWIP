import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.patheffects as pe
import pandas as pd
import matplotlib.cm as cm


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


def plot_3d_colorbar(lat, lon, alt, col):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection="3d")
    sc = ax.scatter(lat, lon, alt, c=col, cmap="jet")
    ax.set_xlabel("lat")
    ax.set_ylabel("lon")
    ax.set_zlabel("alt")
    ax_pos = ax.get_position()
    cbar_ax = fig.add_axes(
        [
            ax_pos.x1 + 0.05,  # x-position: just right of the main axis
            ax_pos.y0,  # y-position: aligned to bottom of main axis
            0.03,  # width
            ax_pos.height,  # height: same as 3D axis
        ]
    )
    cb = fig.colorbar(sc, cax=cbar_ax)
    cb.set_label(col.name)
    ax.set_title(lat.index[0].date())
    plt.show()


def plot_plane_track_with_seeds(df, start_timestamp, aircraft, filename=""):
    plt.rc("font", size=MEDIUM_SIZE)
    df = df.dropna(subset=["lon [deg]", "lat [deg]"])
    country_reader = Reader("shapefiles/gadm41_SAU_1.shp")
    radar_multirings_reader = Reader(
        "shapefiles/RCSP_MultiRings_200/RCSP_MultiRings_200.shp"
    )
    radar_df = pd.read_csv("Operations_radar_info.csv")
    provinces = list(country_reader.geometries())
    n_provinces = len(provinces)
    colors = cm.get_cmap("tab20", n_provinces)  # or "Set3", "tab10", etc.

    projection = ccrs.Mercator()

    fig = plt.figure(figsize=(14, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, 0], projection=projection)
    ax2 = fig.add_subplot(gs[0, 1], projection=projection)

    # Compute zoom extent from the flight track
    padding = 0.5
    min_lon = df["lon [deg]"].min() - padding
    max_lon = df["lon [deg]"].max() + padding + 0.7
    min_lat = df["lat [deg]"].min() - padding
    max_lat = df["lat [deg]"].max() + padding
    zoom_extent = [min_lon, max_lon, min_lat, max_lat]
    ax2.set_extent(zoom_extent, crs=ccrs.PlateCarree())

    # Filter radar locations within the zoom extent
    radars_in_view = radar_df[
        (radar_df["Longitude"] >= min_lon)
        & (radar_df["Longitude"] <= max_lon)
        & (radar_df["Latitude"] >= min_lat)
        & (radar_df["Latitude"] <= max_lat)
    ]

    # Add gridlines and markers
    for ax in [ax1, ax2]:
        gl = ax.gridlines(
            draw_labels=True,
            crs=ccrs.PlateCarree(),
            linewidth=0.5,
            color="gray",
            alpha=0.5,
        )
        gl.top_labels = False
        gl.right_labels = False

    # Add provinces
    for i, geom in enumerate(provinces):
        ax1.add_geometries(
            [geom],
            crs=ccrs.PlateCarree(),
            facecolor=colors(i),
            edgecolor="gray",
            linewidth=0.5,
            alpha=0.6,  # subtle transparency
        )
        ax2.add_geometries(
            [geom],
            crs=ccrs.PlateCarree(),
            facecolor=colors(i),
            edgecolor="gray",
            linewidth=0.5,
            alpha=0.6,  # subtle transparency
        )

    # Plot radar points on ax1
    for _, row in radar_df.iterrows():
        ax1.plot(
            row["Longitude"],
            row["Latitude"],
            marker="^",
            color="blue",
            transform=ccrs.PlateCarree(),
        )
        ax1.text(
            row["Longitude"] + 0.3,  # offset to avoid overlap
            row["Latitude"],
            row["Name"],
            transform=ccrs.PlateCarree(),
            color="k",
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
            fontsize=SMALL_SIZE,
        )

    # Plot radar points on ax2
    for _, row in radars_in_view.iterrows():
        ax2.plot(
            row["Longitude"],
            row["Latitude"],
            marker="^",
            color="blue",
            transform=ccrs.PlateCarree(),
        )
        ax2.text(
            row["Longitude"] + 0.1,  # offset text a little
            row["Latitude"],
            row["Name"],
            transform=ccrs.PlateCarree(),
            color="k",
            fontsize=SMALL_SIZE,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
        )

    shape_feature_radar_multirings = ShapelyFeature(
        radar_multirings_reader.geometries(),
        ccrs.PlateCarree(),
        facecolor="none",
        edgecolor="black",
    )

    # Plot first subplot (full map view)
    ax1.add_feature(shape_feature_radar_multirings)
    ax1.plot(
        df["lon [deg]"],
        df["lat [deg]"],
        transform=ccrs.PlateCarree(),
    )
    ax1.set_extent([34, 56, 16, 33], crs=ccrs.PlateCarree())

    # Plot second subplot (zoomed to track)
    ax2.plot(
        df["lon [deg]"],
        df["lat [deg]"],
        transform=ccrs.PlateCarree(),
    )

    # Get start and stop recording points
    start_rec = df.iloc[0]
    stop_rec = df.iloc[-1]

    # Plot start and stop points
    ax2.plot(
        start_rec["lon [deg]"],
        start_rec["lat [deg]"],
        "go",
        transform=ccrs.PlateCarree(),
        label="rec start",
    )
    ax2.plot(
        stop_rec["lon [deg]"],
        stop_rec["lat [deg]"],
        "ro",
        alpha=0.7,
        transform=ccrs.PlateCarree(),
        label="rec stop",
    )

    # Calculate seed events
    seed_a_events = df["seed-a [cnt]"].diff() > 0
    seed_b_events = df["seed-b [cnt]"].diff() > 0
    seed_a_count = len(df[seed_a_events])
    seed_b_count = len(df[seed_b_events])

    # Plot seed events
    if seed_a_count > 0:
        ax2.plot(
            df.loc[seed_a_events, "lon [deg]"],
            df.loc[seed_a_events, "lat [deg]"],
            ".",
            color="orange",
            transform=ccrs.PlateCarree(),
            label=f"seed-a: {seed_a_count}",
        )
    if seed_b_count > 0:
        ax2.plot(
            df.loc[seed_b_events, "lon [deg]"],
            df.loc[seed_b_events, "lat [deg]"],
            ".",
            color="magenta",
            transform=ccrs.PlateCarree(),
            label=f"seed-b: {seed_b_count}",
        )

    # ax2.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    fig.suptitle(f"{start_timestamp}, {aircraft}")
    # fig.subplots_adjust(wspace=0.05, left=0.05, right=0.88, top=0.92, bottom=0.18)
    margin = 0.07
    fig.subplots_adjust(
        wspace=0.05, left=margin, right=1 - margin, top=0.92, bottom=0.16
    )
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=len(handles),
        bbox_to_anchor=(0.5, 0.0),
    )
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_scatter_map(df, col):
    reader = Reader("shapefiles/gadm41_SAU_1.shp")
    projection = ccrs.Mercator()
    plt.figure(figsize=(6, 4))
    plt.rc("font", size=MEDIUM_SIZE)
    ax = plt.axes(projection=projection)
    shape_feature = ShapelyFeature(
        reader.geometries(),
        ccrs.PlateCarree(),
        facecolor="none",
        edgecolor="black",
    )
    ax.add_feature(shape_feature)
    ax.set_extent([34, 56, 16, 33], crs=ccrs.PlateCarree())
    scatter = ax.scatter(
        df["lon [deg]"],
        df["lat [deg]"],
        s=8,
        c=df[col],
        cmap="jet",
        transform=ccrs.PlateCarree(),
    )
    cb = plt.colorbar(scatter, ax=ax)
    cb.set_label(col)
    plt.tight_layout()
    plt.show()


def plot_hist(df, col, filename=""):
    plt.figure(figsize=(6, 4))
    plt.hist(df[col], bins=50, edgecolor="k")
    plt.rc("font", size=MEDIUM_SIZE)
    plt.xlabel(col)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_temp_ss_seed_ab(df):
    seed_a = df[(df["seed-a [cnt]"].diff() > 0)]
    seed_b = df[(df["seed-b [cnt]"].diff() > 0)]
    temp_a = seed_a["Ambient Temperature (C)"]
    temp_b = seed_b["Ambient Temperature (C)"]
    ss_a = seed_a["ss_total [%]"]
    ss_b = seed_b["ss_total [%]"]
    plt.rc("font", size=MEDIUM_SIZE)
    plt.scatter(ss_b, temp_b, edgecolor="k", label="seed-b")
    plt.scatter(ss_a, temp_a, edgecolor="k", label="seed-a")
    plt.ylabel("Ambient Temperature (C)")
    plt.gca().invert_yaxis()
    plt.xlabel("ss_total [%]")
    plt.legend()
    plt.show()


def plot_scatter(df, x, y, filename="", title=""):
    plt.rc("font", size=MEDIUM_SIZE)
    plt.scatter(df[x], df[y], edgecolor="k")
    # plt.xlim(-3,7)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_scatter_gif(df_list, x, y, filename=""):
    ss_min, ss_max = 0, 100
    temp_min, temp_max = -17, 12

    fig, ax = plt.subplots()
    plt.rc("font", size=MEDIUM_SIZE)

    def update(frame):
        ax.clear()
        ax.invert_yaxis()
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_xlim(ss_min, ss_max)
        ax.set_ylim(temp_max, temp_min)

        past_alpha = 0.2
        current_alpha = 1.0
        color = "C0"

        # Plot all previous frames with faded alpha
        for i in range(frame):
            df = df_list[i]
            ax.scatter(
                df[x], df[y], color=color, alpha=past_alpha, edgecolor="k"
            )
        # Plot current frame with full alpha
        df = df_list[frame]
        ax.scatter(
            df[x], df[y], color=color, alpha=current_alpha, edgecolor="k"
        )
        ax.set_title(df.index[0].date())
        fig.tight_layout()
        return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(df_list), blit=False, repeat=False
    )
    if filename:
        ani.save(filename, writer="pillow", fps=1)
    plt.show()


def plot_bar(df, col):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(df.index, df[col], edgecolor="black")
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="-", linewidth=0.8, alpha=0.8)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.set_ylabel(col)
    plt.rc("font", size=MEDIUM_SIZE)
    plt.show()


def plot_bar_stacked(df, col1, col2):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(df.index, df[col1], label=col1, edgecolor="black")
    ax.bar(df.index, df[col2], bottom=df[col1], label=col2, edgecolor="black")
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="-", linewidth=0.8, alpha=0.8)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.legend()
    plt.rc("font", size=MEDIUM_SIZE)
    plt.show()
