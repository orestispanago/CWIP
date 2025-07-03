import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.animation as animation
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


def plot_scatter(df, x, y, filename=""):
    plt.rc("font", size=MEDIUM_SIZE)
    plt.scatter(df[x], df[y], edgecolor="k")
    # plt.xlim(-3,7)
    plt.xlabel(x)
    plt.ylabel(y)
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
