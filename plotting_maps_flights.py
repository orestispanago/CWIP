import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import matplotlib.patheffects as pe
from utils.plotting import MEDIUM_SIZE, SMALL_SIZE, savefig
from plotting_maps import (
    plot_plane_track,
    plot_seeds,
    plot_start_stop,
    projection,
    radar_df,
    provinces,
    province_colors,
    radar_multirings_reader,
)


import seaborn as sns
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import numpy.ma as ma
from plotting_maps import (
    create_map_axes,
    plot_gridlines_and_labels,
    plot_multirings,
    plot_provinces,
    plot_radar_locations,
)
from utils.plotting import savefig


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

    fig = plt.figure(figsize=(14, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, 0], projection=projection)
    ax2 = fig.add_subplot(gs[0, 1], projection=projection)

    ax1.set_extent([34, 56, 16, 33])
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

    for ax in [ax1, ax2]:
        plot_gridlines_and_labels(ax)

    plot_provinces(ax1, facecolors="provinces")
    plot_radar_locations(ax1, labels=True)
    plot_multirings(ax1)
    plot_plane_track(df, ax1)
    plot_start_stop(df, ax1)

    # Plot map on ax2 zoomed to track
    plot_provinces(ax2, facecolors="provinces")
    plot_radar_locations(ax2, df=radars_in_view, labels=True)
    plot_plane_track(df, ax2)
    plot_start_stop(df, ax2)

    seed_a_events = df[df["seed-a [cnt]"].diff() > 0]
    seed_b_events = df[df["seed-b [cnt]"].diff() > 0]

    plot_seeds(seed_a_events, ax2, marker=".")
    plot_seeds(seed_b_events, ax2, color="magenta", marker=".")

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
    savefig(filename)
    plt.show()
