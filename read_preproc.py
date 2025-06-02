import glob
import pandas as pd
from plotting import (
    plot_3d_colorbar,
    plot_hist,
    plot_scatter,
    plot_scatter_gif,
    plot_scatter_map,
    plot_temp_ss_seed_ab,
    plot_timeseries,
)
import matplotlib.pyplot as plt


flights = glob.glob("*/*/*/*/")

seed = []
for flight in flights[:10]:
    adc_fname = glob.glob(f"{flight}/*adc.csv")[0]
    fin_fname = glob.glob(f"{flight}/*fin.csv")[0]
    wind_fname = glob.glob(f"{flight}/*wind.csv")[0]

    fin = pd.read_csv(fin_fname, parse_dates=True, index_col="datetime")
    wind = pd.read_csv(wind_fname, parse_dates=True, index_col="datetime")
    adc = pd.read_csv(adc_fname, parse_dates=True, index_col="datetime")

    fin.index.round("s")
    wind.index = wind.index.round("s")

    fin = fin[~fin.index.duplicated(keep="first")]
    wind = wind[~wind.index.duplicated(keep="first")]

    merged = pd.concat([fin, wind], axis=1)

    lat = merged["lat [deg]"]
    lon = merged["lon [deg]"]
    alt = merged["gps_alt [m]"]
    temp = merged["Ambient Temperature (C)"]
    lwc = merged["LWC (g/m^3)"]

    # plot_3d_colorbar(lat, lon, alt, lwc)

    if (merged["seed-a [cnt]"].max() > 0) or (merged["seed-b [cnt]"].max() > 0):
        seed.append(merged)

seed_merged = pd.concat(seed)

# seed_merged = seed_merged[seed_merged["LWC (g/m^3)"] > 0]
# seed_merged = seed_merged[seed_merged["Ambient Temperature (C)"] < 0]


seed_locations = seed_merged[
    (seed_merged["seed-a [cnt]"].diff() > 0)
    | (seed_merged["seed-b [cnt]"].diff() > 0)
]

# lat = seed_locations["lat [deg]"]
# lon = seed_locations["lon [deg]"]
# plot_scatter_map(seed_locations, "ss_total [%]")


# plot_hist(seed_locations, "ss_total [%]")
# plot_hist(seed_locations, "ss_temp [%]")
# plot_hist(seed_locations, "ss_rh [%]")
# plot_hist(seed_locations, "ss_lwc [%]")
# plot_hist(seed_locations, "ss_updraft [%]")

# plot_temp_ss_seed_ab(seed_merged)


# dfs_by_date = [
#     group for _, group in seed_locations.groupby(seed_locations.index.date)
# ]
# plot_scatter_gif(
#     dfs_by_date,
#     "ss_total [%]",
#     "Ambient Temperature (C)",
#     filename="temp_ss_scatter.gif",
# )

# plot_scatter(seed_locations, "ss_total [%]", "Ambient Temperature (C)")

# plot_scatter(seed_locations, "temp_amb [C]", "ss_temp [%]")

# plot_scatter(seed_locations, "rh [%]", "ss_rh [%]")

# plot_scatter(seed_locations, "lwc [g/m^3]", "ss_lwc [%]")

# plot_scatter(seed_locations, "wind_w [m/s]", "ss_updraft [%]")

# plot_scatter(seed_locations, "attack [deg]", "ss_updraft [%]")

seed_merged_by_date = [
    group for _, group in seed_merged.groupby(seed_merged.index.date)
]
for df in seed_merged_by_date:
    plot_timeseries(df, "Ambient Temperature (C)")
    plot_timeseries(df, "LWC (g/m^3)")
    plot_timeseries(df, "gps_alt [m]")
