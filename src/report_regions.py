import os
import glob
import pandas as pd
from utils.utils import select_seed_locations
from plotting_maps_regions import (
    plot_map_kde_periods,
    plot_map_seed_periods,
    plot_map_seed_regions,
    plot_map_kde_single_period,
    plot_grid_percentage,
)
from data_readers import read_wind_csv
from utils.regions import SeparatorLine, classify_regions
from config import SPLIT_DATA, MAPS

wind_files = glob.glob(f"{SPLIT_DATA}/**/*wind.csv", recursive=True)
df_list = []
for wind_file in wind_files:
    wind = read_wind_csv(wind_file)
    period = wind["period"].values[0]
    df_list.append(wind)

all_wind = pd.concat(df_list)
seed_locations = select_seed_locations(all_wind)

sep = SeparatorLine()

seed_locations = classify_regions(seed_locations, sep.slope, sep.intercept)

plot_map_seed_regions(
    seed_locations,
    sep,
    extent="country",
    filename=f"{MAPS}/maps_regions_separation.png",
)
plot_map_seed_periods(
    seed_locations, extent="country", filename=f"{MAPS}/map_periods.png"
)

plot_map_kde_periods(
    seed_locations, extent="country", filename=f"{MAPS}/map_kde_periods.png"
)

for period in seed_locations["period"].unique():
    period_df = seed_locations[seed_locations["period"] == period]
    plot_map_kde_single_period(
        period_df,
        title=period,
        extent="country",
        filename=f"{MAPS}/kde/map_kde_{period}.png",
    )

    grid = 0.5  # degrees
    plot_grid_percentage(
        period_df,
        grid=grid,
        extent="country",
        title=f"{period}, grid: {grid}",
        filename=f"{MAPS}/grid/map_grid{grid} {period}.png",
    )
