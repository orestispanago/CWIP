import seaborn as sns
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.patheffects as pe
import pandas as pd

SMALL_SIZE = 8
MEDIUM_SIZE = 14

country_reader = Reader("shapefiles/KSA/gadm41_SAU_1.shp")
radar_multirings_reader = Reader(
    "shapefiles/RCSP_MultiRings_200/RCSP_MultiRings_200.shp"
)
radar_df = pd.read_csv("shapefiles/operations_radar_locations.csv")
provinces = list(country_reader.geometries())
n_provinces = len(provinces)
province_colors = plt.get_cmap("tab20", n_provinces)  # or "Set3", "tab10", etc.
projection = ccrs.Mercator()


def create_map_axes():
    plt.figure(figsize=(8, 7))
    plt.rc("font", size=MEDIUM_SIZE)
    ax = plt.axes(projection=projection)
    ax.set_extent([34, 56, 16, 33], crs=ccrs.PlateCarree())
    return ax


def plot_provinces(ax, facecolors=None, zorder=0):
    for i, geom in enumerate(provinces):
        if facecolors:
            facecolor = province_colors(i)
        else:
            facecolor = "white"
        ax.add_geometries(
            [geom],
            crs=ccrs.PlateCarree(),
            facecolor=facecolor,
            edgecolor="gray",
            linewidth=0.5,
            zorder=zorder,
            alpha=0.6,
        )


def plot_radar_locations(ax, labels=False, zorder=10):
    for _, row in radar_df.iterrows():
        ax.scatter(
            row["Longitude"],
            row["Latitude"],
            marker="^",
            color="blue",
            edgecolors="k",
            zorder=zorder,
            transform=ccrs.PlateCarree(),
        )
        if labels:
            ax.text(
                row["Longitude"] + 0.3,  # offset to avoid overlap
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


def plot_map_seed_regions(df, sep_line=None, filename=""):
    ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors=province_colors)
    plot_radar_locations(ax)
    plot_multirings(ax)

    # Plot the diagonal line
    if sep_line:
        ax.plot(
            sep_line.lons,
            sep_line.lats,
            color="black",
            linewidth=2,
            linestyle="--",
            transform=ccrs.PlateCarree(),
        )
    region_colors = {
        "Central": "red",
        "SW": "green",
    }
    colors = df["region"].map(region_colors)
    ax.scatter(
        df["lon [deg]"],
        df["lat [deg]"],
        s=20,
        color=colors,
        edgecolors="k",
        linewidths=0.5,
        alpha=0.5,
        zorder=5,
        transform=ccrs.PlateCarree(),
    )
    for region, color in region_colors.items():
        ax.scatter([], [], color=color, label=region, edgecolors="k")
    ax.legend(title="Region")
    plt.title("Fall 2024 - Spring 2025")
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_map_seed_periods(df, sep_line=None, filename=""):
    ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors=province_colors)
    plot_radar_locations(ax)
    plot_multirings(ax)
    # Plot the diagonal line
    if sep_line:
        ax.plot(
            sep_line.lons,
            sep_line.lats,
            color="black",
            linewidth=2,
            linestyle="--",
            transform=ccrs.PlateCarree(),
        )
    region_colors = {
        "Spring": "red",
        "Fall": "green",
    }
    colors = df["period"].map(region_colors)
    ax.scatter(
        df["lon [deg]"],
        df["lat [deg]"],
        s=20,
        color=colors,
        edgecolors="k",
        linewidths=0.5,
        alpha=0.1,
        zorder=5,
        transform=ccrs.PlateCarree(),
    )
    for period, color in region_colors.items():
        ax.scatter([], [], color=color, label=period, edgecolors="k")
    ax.legend(title="Operational period")
    plt.title("Fall 2024 - Spring 2025")
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_map_kde_periods(df, filename=""):
    ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors=province_colors)
    plot_radar_locations(ax, labels=True)
    plot_multirings(ax)

    period_colors = {
        "Spring": "green",
        "Fall": "red",
    }
    legend_handles = []
    for period, color in period_colors.items():
        subset = df[df["period"] == period]
        sns.kdeplot(
            x=subset["lon [deg]"],
            y=subset["lat [deg]"],
            ax=ax,
            color=color,
            alpha=0.6,
            bw_adjust=0.5,
            levels=10,
            linewidths=1,
            transform=ccrs.PlateCarree(),
            zorder=5,
        )
        legend_handles.append(Patch(facecolor=color, label=period))
    ax.legend(handles=legend_handles, title="Operational period")
    plt.title("Fall 2024 - Spring 2025")
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()
