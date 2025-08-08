import glob
import pandas as pd
from readers import read_wind_csv
from utils import select_seed_locations
from regions_utils import SeparatorLine, classify_regions
from calendars_plotting import (
    calplot_planes_per_day,
    calplot_seed_events,
    calplot_regions_per_day,
)

wind_files = glob.glob("*/*/*/*/*wind.csv")

df_list = []
for wind_file in wind_files:
    wind = read_wind_csv(wind_file)
    df_list.append(wind)
all_wind = pd.concat(df_list)

sep = SeparatorLine()
seed_locations = select_seed_locations(all_wind)

wind_classified = classify_regions(all_wind, sep.slope, sep.intercept)


calplot_seed_events(
    seed_locations, filename="plots/calplots/calplot_seed_events.png"
)
calplot_planes_per_day(
    wind_classified, filename="plots/calplots/calplot_planes.png"
)

calplot_regions_per_day(
    wind_classified, filename="plots/calplots/calplot_regions.png"
)
