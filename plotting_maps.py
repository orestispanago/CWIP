import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.patheffects as pe
import pandas as pd

from utils.plotting import SMALL_SIZE, MEDIUM_SIZE


country_reader = Reader("data/shapefiles/KSA/gadm41_SAU_1.shp")
radar_multirings_reader = Reader(
    "data/shapefiles/RCSP_MultiRings_200/RCSP_MultiRings_200.shp"
)
radar_df = pd.read_csv("data/shapefiles/operations_radar_locations.csv")
provinces = list(country_reader.geometries())
n_provinces = len(provinces)
province_colors = plt.get_cmap("tab20", n_provinces)  # or "Set3", "tab10", etc.
projection = ccrs.PlateCarree()


def create_map_axes(facecolor="", extent=""):
    fig, ax = plt.subplots(
        figsize=(8, 7), subplot_kw=dict(projection=projection)
    )
    plt.rc("font", size=MEDIUM_SIZE)
    country_extent = [34, 56, 16, 33]
    if not extent:
        pass  # Let Cartopy autoscale to data
    elif extent == "country":
        ax.set_extent(country_extent, crs=projection)
    else:
        ax.set_extent(extent, crs=projection)
    if facecolor:
        ax.set_facecolor(facecolor)
    return fig, ax


def plot_provinces(ax, facecolors="white", alpha=0.6, zorder=0):
    for i, geom in enumerate(provinces):
        if facecolors == "provinces":
            facecolor = province_colors(i)
        else:
            facecolor = facecolors
        ax.add_geometries(
            [geom],
            crs=ccrs.PlateCarree(),
            facecolor=facecolor,
            edgecolor="gray",
            linewidth=0.5,
            zorder=zorder,
            alpha=alpha,
        )


def filter_points_by_extent(ax, df):
    xmin, xmax, ymin, ymax = ax.get_extent()
    in_extent = (
        (df["Longitude"] >= xmin)
        & (df["Longitude"] <= xmax)
        & (df["Latitude"] >= ymin)
        & (df["Latitude"] <= ymax)
    )
    return df[in_extent]


def plot_radar_locations(
    ax, df=radar_df, labels=False, label_offset=0.3, zorder=10
):
    for _, row in df.iterrows():
        ax.scatter(
            row["Longitude"],
            row["Latitude"],
            marker="^",
            s=40,
            color="blue",
            edgecolors="k",
            zorder=zorder,
            transform=ccrs.PlateCarree(),
        )
        if labels:
            ax.text(
                row["Longitude"] + label_offset,  # offset to avoid overlap
                row["Latitude"],
                row["Name"],
                transform=ccrs.PlateCarree(),
                color="k",
                zorder=zorder,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")],
                fontsize=SMALL_SIZE,
            )


def plot_multirings(ax):
    shape_feature_radar_multirings = ShapelyFeature(
        radar_multirings_reader.geometries(),
        ccrs.PlateCarree(),
        facecolor="none",
        edgecolor="black",
    )
    ax.add_feature(shape_feature_radar_multirings)


def plot_gridlines_and_labels(ax):
    gl = ax.gridlines(
        draw_labels=True,
        crs=ccrs.PlateCarree(),
        linewidth=0.5,
        color="gray",
        alpha=0.5,
    )
    gl.top_labels = False
    gl.right_labels = False


def plot_plane_track(df, ax):
    ax.plot(
        df["lon [deg]"],
        df["lat [deg]"],
        # s=1,
        # edgecolors="k",
        linewidth=1,
        # alpha=0.5,
        zorder=5,
        transform=ccrs.PlateCarree(),
    )


def plot_start_stop(df, ax):
    start_rec = df.iloc[0]
    stop_rec = df.iloc[-1]
    ax.scatter(
        start_rec["lon [deg]"],
        start_rec["lat [deg]"],
        s=50,
        color="green",
        alpha=0.7,
        transform=ccrs.PlateCarree(),
        label="rec start",
        zorder=5,
    )
    ax.scatter(
        stop_rec["lon [deg]"],
        stop_rec["lat [deg]"],
        s=50,
        color="red",
        alpha=0.7,
        transform=ccrs.PlateCarree(),
        label="rec stop",
        zorder=5,
    )


def plot_seeds(df, ax, color="green", marker="_"):
    ax.scatter(
        df["lon [deg]"],
        df["lat [deg]"],
        marker=marker,
        s=20,
        color=color,
        linewidths=1,
        zorder=5,
        transform=ccrs.PlateCarree(),
        label=f"Seed events: {len(df)}",
    )
