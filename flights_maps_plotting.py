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


def plot_flight_3d_colorbar(lat, lon, alt, col):
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
    country_reader = Reader("shapefiles/KSA/gadm41_SAU_1.shp")
    radar_multirings_reader = Reader(
        "shapefiles/RCSP_MultiRings_200/RCSP_MultiRings_200.shp"
    )
    radar_df = pd.read_csv("shapefiles/operations_radar_locations.csv")
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
