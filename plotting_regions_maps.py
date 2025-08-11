import seaborn as sns
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.patheffects as pe
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np
import numpy.ma as ma
from utils_plotting import SMALL_SIZE, MEDIUM_SIZE



country_reader = Reader("shapefiles/KSA/gadm41_SAU_1.shp")
radar_multirings_reader = Reader(
    "shapefiles/RCSP_MultiRings_200/RCSP_MultiRings_200.shp"
)
radar_df = pd.read_csv("shapefiles/operations_radar_locations.csv")
provinces = list(country_reader.geometries())
n_provinces = len(provinces)
province_colors = plt.get_cmap("tab20", n_provinces)  # or "Set3", "tab10", etc.
projection = ccrs.PlateCarree()


def create_map_axes(facecolor=""):
    fig, ax = plt.subplots(
        figsize=(8, 7), subplot_kw=dict(projection=projection)
    )
    plt.rc("font", size=MEDIUM_SIZE)
    ax = plt.axes(projection=projection)
    ax.set_extent([34, 56, 16, 33], crs=projection)
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
    fig, ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors="provinces")
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
    fig, ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors="provinces")
    plot_radar_locations(ax)
    plot_multirings(ax)
    region_colors = {
        "Spring 2025": "red",
        "Fall 2024": "green",
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
    fig, ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors="provinces")
    plot_radar_locations(ax, labels=True)
    plot_multirings(ax)

    period_colors = {
        "Spring 2025": "green",
        "Fall 2024": "red",
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


def plot_map_kde_single_period(df, filename="", title=""):
    fig, ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax)
    plot_radar_locations(ax, labels=True)
    plot_multirings(ax)

    # KDE plot
    kde = sns.kdeplot(
        x=df["lon [deg]"],
        y=df["lat [deg]"],
        ax=ax,
        fill=True,
        cmap="hot",
        bw_adjust=0.5,
        thresh=0.05,
        levels=10,
    )

    plt.title(title)

    # Add colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05, axes_class=plt.Axes)

    # Create a ScalarMappable for the colorbar
    norm = plt.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap="hot", norm=norm)
    sm.set_array([])

    # Create colorbar using the ScalarMappable
    cbar = fig.colorbar(sm, cax=cax)
    # cbar.set_ticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    cbar.set_label("Seed event density", rotation=270, labelpad=15)
    plt.tight_layout()
    if filename:
        plt.savefig(filename, bbox_inches="tight")
    plt.show()


def plot_grid_percentage(df, grid=0.5, filename="", title=""):
    fig, ax = create_map_axes()
    plot_gridlines_and_labels(ax)
    plot_provinces(ax)
    plot_radar_locations(ax, labels=True)
    plot_multirings(ax)

    # Define grid resolution (e.g., 0.5° × 0.5° cells)
    grid_size = grid
    lon_bins = np.arange(34, 56 + grid_size, grid_size)
    lat_bins = np.arange(16, 33 + grid_size, grid_size)

    # Count flares per grid cell
    counts, xedges, yedges = np.histogram2d(
        df["lon [deg]"], df["lat [deg]"], bins=[lon_bins, lat_bins]
    )

    # Calculate percentages (flares per cell / total flares)
    total_flares = counts.sum()
    percentages = (counts / total_flares) * 100  # Convert to %
    percentages_masked = ma.masked_where(percentages == 0, percentages)

    mesh = ax.pcolormesh(
        xedges,
        yedges,
        percentages_masked.T,
        cmap="hot",
        shading="auto",
        transform=ccrs.PlateCarree(),
        vmin=0,
        vmax=20,
    )
    plt.title(title)
    # Add colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05, axes_class=plt.Axes)
    cbar = fig.colorbar(mesh, cax=cax)
    cbar.set_label(
        "Seed events per cell / total (%)", rotation=270, labelpad=15
    )

    plt.tight_layout()
    if filename:
        plt.savefig(filename, bbox_inches="tight")
    plt.show()
