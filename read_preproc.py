import glob
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from pandas.errors import InvalidIndexError


# _, period, aircraft,_, base_name = fin_fname.split(os.sep)
# date_time_str = base_name.split("_")[1]
# date_time = datetime.strptime(date_time_str, "%Y%m%d%H%M%S")
# date = date_time.date()

def plot_3d_colorbar(lat,lon,alt,col):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    sc = ax.scatter(lat, lon, alt, c=lwc, cmap='jet')
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

flights=glob.glob("*/*/*/*/")

for flight in flights:
    adc_fname = glob.glob(f"{flight}/*adc.csv")[0]
    fin_fname = glob.glob(f"{flight}/*fin.csv")[0]
    wind_fname = glob.glob(f"{flight}/*wind.csv")[0]
    
    fin=pd.read_csv(fin_fname, parse_dates=True, index_col="datetime")
    wind=pd.read_csv(wind_fname, parse_dates=True, index_col="datetime")
    adc=pd.read_csv(adc_fname, parse_dates=True, index_col="datetime")
    
    fin.index.round("s")
    wind.index=wind.index.round("s")
    
    fin = fin[~fin.index.duplicated(keep='first')]
    wind = wind[~wind.index.duplicated(keep='first')]
    
    merged = pd.concat([fin, wind], axis=1)
    
    
    lat = merged["lat [deg]"]
    lon = merged["lon [deg]"]
    alt = merged["gps_alt [m]"]
    temp = merged["Ambient Temperature (C)"]
    lwc = merged["LWC (g/m^3)"]

    plot_3d_colorbar(lat, lon, alt, lwc)
