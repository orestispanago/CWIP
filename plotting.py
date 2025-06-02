import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.animation as animation


SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42

def plot_timeseries(df, col):
    plt.figure(figsize=(10, 4))
    plt.plot(df[col])
    plt.ylabel(col)
    plt.show()

def plot_3d_colorbar(lat,lon,alt,col):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    sc = ax.scatter(lat, lon, alt, c=col, cmap='jet')
    ax.set_xlabel("lat")
    ax.set_ylabel("lon")
    ax.set_zlabel("alt")    
    ax_pos = ax.get_position()
    cbar_ax = fig.add_axes([
        ax_pos.x1 + 0.05,  # x-position: just right of the main axis
        ax_pos.y0,         # y-position: aligned to bottom of main axis
        0.03,              # width
        ax_pos.height      # height: same as 3D axis
    ])
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
    reader.geometries(), ccrs.PlateCarree(), facecolor="none", edgecolor="black")
    ax.add_feature(shape_feature)
    ax.set_extent([34, 56, 16, 33], crs=ccrs.PlateCarree())
    scatter = ax.scatter(
        df["lon [deg]"], df["lat [deg]"],s=8, c=df[col], 
        cmap='jet', transform=ccrs.PlateCarree()
    )
    cb = plt.colorbar(scatter, ax=ax)
    cb.set_label(col)
    plt.tight_layout()
    plt.show()


def plot_hist(df, col):
    plt.figure(figsize=(6, 4))
    plt.hist(df[col], bins=50, edgecolor="k")
    plt.rc("font", size=MEDIUM_SIZE)
    plt.xlabel(col)
    plt.tight_layout()
    plt.show()

def plot_temp_ss_seed_ab(df):
    seed_a = df[(df["seed-a [cnt]"].diff()>0)]
    seed_b = df[(df["seed-b [cnt]"].diff()>0)]
    temp_a =  seed_a["Ambient Temperature (C)"]
    temp_b =  seed_b["Ambient Temperature (C)"]
    ss_a = seed_a['ss_total [%]']
    ss_b = seed_b['ss_total [%]']
    plt.rc("font", size=MEDIUM_SIZE)
    plt.plot(ss_a, temp_a, ".", label="seed-a")
    plt.plot(ss_b, temp_b, ".", label="seed-b")
    plt.ylabel("Ambient Temperature (C)")
    plt.gca().invert_yaxis()
    plt.xlabel("ss_total [%]")
    plt.legend()
    plt.show()

def plot_scatter(df, x, y):
    plt.rc("font", size=MEDIUM_SIZE)
    plt.scatter(df[x], df[y], edgecolor="k")
    # plt.xlim(-3,7)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

def plot_scatter_gif(df_list, x, y, filename=""):
    ss_min, ss_max = 0, 100
    temp_min, temp_max = -12, 0
    
    fig, ax = plt.subplots(figsize=(10, 7))
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
        color = 'blue'
        
        # Plot all previous frames with faded alpha
        for i in range(frame):
            df = df_list[i]
            ax.scatter(df[x], df[y], color=color, alpha=past_alpha)
        # Plot current frame with full alpha
        df = df_list[frame]
        ax.scatter( df[x], df[y], color=color, alpha=current_alpha)
        ax.set_title(df.index[0].date())
        return []
    ani = animation.FuncAnimation(fig, update, frames=len(df_list),
                                  blit=False, repeat=False)
    if filename:
        ani.save(filename, writer='pillow', fps=1)
    plt.show()