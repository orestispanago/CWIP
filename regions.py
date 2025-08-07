import glob
import pandas as pd
from maps_plotting import (
    plot_map_kde_periods,
    plot_map_seed_regions,
    plot_map_seed_periods,
)
from readers import read_wind_csv
import numpy as np


class SeparatorLine:
    def __init__(self, x1=39, y1=25, x2=48, y2=20):
        self.start = (x1, y1)
        self.end = (x2, y2)
        self.lons = [x1, x2]
        self.lats = [y1, y2]
        self.slope = (y2 - y1) / (x2 - x1)
        self.intercept = y1 - self.slope * x1


def classify_regions(df, sep_slope, sep_intercept):
    df["region"] = np.where(
        df["lat [deg]"] > sep_slope * df["lon [deg]"] + sep_intercept,
        "Central",
        "SW",
    )
    return df


def select_seed_locations(df):
    return df[
        (df["seed-a [cnt]"].diff() > 0) | (df["seed-b [cnt]"].diff() > 0)
    ].copy()


wind_files = glob.glob("*/*/*/*/*wind.csv")


df_list = []
for wind_file in wind_files:
    print(wind_file)
    wind = read_wind_csv(wind_file)
    wind["period"] = "Spring" if "Spring" in wind_file else "Fall"
    df_list.append(wind)

all_wind = pd.concat(df_list)
seed_locations = select_seed_locations(all_wind)

sep = SeparatorLine()

seed_locations = classify_regions(seed_locations, sep.slope, sep.intercept)

plot_map_seed_regions(seed_locations, sep, filename="plots/maps/maps_regions_separation.png")
plot_map_seed_periods(seed_locations, sep, filename="plots/maps/map_periods.png")

plot_map_kde_periods(seed_locations, filename="plots/maps/map_kde_periods.png")
