import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patheffects as pe

from plotting_maps import (
    create_map_axes,
    filter_points_by_extent,
    plot_gridlines_and_labels,
    plot_multirings,
    plot_plane_track,
    plot_provinces,
    plot_radar_locations,
    SMALL_SIZE,
    plot_seeds,
    radar_df,
)
from utils.plotting import savefig


def plot_penetrations(df, ax):
    ax.scatter(
        df["lon [deg]"],
        df["lat [deg]"],
        marker=",",
        s=20,
        color="orange",
        # edgecolors="k",
        # linewidths=0.5,
        # alpha=0.5,
        zorder=5,
        transform=ccrs.PlateCarree(),
        label=f"Cloud penetrations: {len(df)}",
    )
    for _, row in df.iterrows():
        ax.text(
            row["lon [deg]"] + 0.01,  # offset to avoid overlap
            row["lat [deg]"],
            f'p{row["pen_id"]}',
            transform=ccrs.PlateCarree(),
            color="k",
            zorder=5,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
            fontsize=SMALL_SIZE,
        )


def plot_flight_track_with_seeds(
    df, seeds, filename="", title="", extent="", radar_label_offset=0.1
):
    fig, ax = create_map_axes(extent=extent)
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors="white")

    plot_multirings(ax)
    plot_plane_track(df, ax)

    # plot_start_stop(df, ax)

    plot_seeds(seeds, ax)

    radars_in_extent = filter_points_by_extent(ax, radar_df)
    plot_radar_locations(
        ax, df=radars_in_extent, labels=True, label_offset=radar_label_offset
    )

    # plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)
    plt.title(title)
    plt.tight_layout()
    savefig(filename)
    plt.show()


def plot_flight_track_with_pens_and_seeds(
    df, seeds, pens, filename="", title="", extent="", radar_label_offset=0.1
):
    fig, ax = create_map_axes(extent=extent)
    plot_gridlines_and_labels(ax)
    plot_provinces(ax, facecolors="white")

    plot_multirings(ax)
    plot_plane_track(df, ax)

    # plot_start_stop(df, ax)

    plot_penetrations(pens, ax)

    plot_seeds(seeds, ax)

    radars_in_extent = filter_points_by_extent(ax, radar_df)
    plot_radar_locations(
        ax, radars_in_extent, labels=True, label_offset=radar_label_offset
    )

    # plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)
    plt.title(title)
    plt.tight_layout()
    savefig(filename)
    plt.show()
