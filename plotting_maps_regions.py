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
from utils_plotting import savefig


def plot_map_seed_regions(df, sep_line=None, filename="", **kwargs):
    fig, ax = create_map_axes(**kwargs)
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
    savefig(filename)
    plt.show()


def plot_map_seed_periods(df, filename="", extent=""):
    fig, ax = create_map_axes(extent=extent)
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
    savefig(filename)
    plt.show()


def plot_map_kde_periods(df, filename="", extent=""):
    fig, ax = create_map_axes(extent=extent)
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
    savefig(filename)
    plt.show()


def plot_map_kde_single_period(df, filename="", title="", extent=""):
    fig, ax = create_map_axes(extent=extent)
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
    savefig(filename)
    plt.show()


def plot_grid_percentage(df, grid=0.5, filename="", title="", extent=""):
    fig, ax = create_map_axes(extent=extent)
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
    savefig(filename)
    plt.show()
