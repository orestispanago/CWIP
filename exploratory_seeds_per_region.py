import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.patheffects as pe
import pandas as pd
from utils_plotting import SMALL_SIZE, MEDIUM_SIZE
from utils import select_seed_locations
from plotting_case_study_map import plot_flight_track_with_seeds

from data_readers import read_wind_csv

country_reader = Reader("shapefiles/KSA/gadm41_SAU_1.shp")
radar_multirings_reader = Reader(
    "shapefiles/RCSP_MultiRings_200/RCSP_MultiRings_200.shp"
)
radar_df = pd.read_csv("shapefiles/operations_radar_locations.csv")
provinces = list(country_reader.geometries())
n_provinces = len(provinces)
province_colors = plt.get_cmap("tab20", n_provinces)  # or "Set3", "tab10", etc.
projection = ccrs.PlateCarree()

wind_file = ("split/Spring 2025/CS4/20250429120855/cwip_CS4_20250429120855_wind.csv")
# wind_file = ("split/Spring 2025/CS2/20250429051654/cwip_CS2_20250429051654_wind.csv")


wind_df = read_wind_csv(wind_file)
seeds = select_seed_locations(wind_df)

plot_flight_track_with_seeds(wind_df, seeds)


import geopandas as gpd
gdf_provinces = gpd.read_file("shapefiles/KSA/gadm41_SAU_1.shp")

wind_gdf = gpd.GeoDataFrame(
    wind_df,
    geometry=gpd.points_from_xy(wind_df["lon [deg]"], wind_df["lat [deg]"]),
    crs="EPSG:4326"  # assuming lat/lon in WGS84
)

gdf_provinces = gdf_provinces.to_crs(wind_gdf.crs)


wind_with_province = gpd.sjoin(
    wind_gdf,
    gdf_provinces[["NAME_1", "geometry"]],
    how="inner",
    predicate="within"
)

wind_with_province = wind_with_province.rename(columns={"NAME_1": "province"})
plot_flight_track_with_seeds(wind_with_province, seeds)