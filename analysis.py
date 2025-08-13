import glob
import pandas as pd
from plotting_analysis import *
from scipy import stats


def filter_slamfire(df, time_threshold=2):
    filtered_list = []
    seed_locations_merged_by_date = [
        group for _, group in df.groupby(df.index.date)
    ]
    for day in seed_locations_merged_by_date:
        last_column = df.iloc[:, -1]  # last column is named aircraft
        seed_by_plane = [group for _, group in day.groupby(last_column)]
        for plane in seed_by_plane:
            time_diffs = plane.index.to_series().diff().dt.total_seconds()
            filtered_df = plane[time_diffs < time_threshold]
            if len(filtered_df) > 0:
                filtered_list.append(filtered_df)
    return filtered_list


def get_rows_before_seed(df, seconds=10):
    seed_locations = df[
        (df["seed-a [cnt]"].diff() == 1) | (df["seed-b [cnt]"].diff() == 1)
    ]
    # For each change time, select rows within the 10 minutes before it
    rows_before_changes = []
    for change_time in seed_locations.index:
        mask = (
            seed_merged.index >= change_time - pd.Timedelta(seconds=seconds)
        ) & (seed_merged.index < change_time)
        rows_before_changes.append(seed_merged.loc[mask])
    return pd.concat(rows_before_changes).drop_duplicates()


def filter_data(df):
    print(f"Total: {len(df)}")
    filtered = df.loc[df["lwc [g/m^3]"] >= 0]
    print(f"LWC >= 0: {len(filtered)}")
    filtered = filtered.loc[filtered["rh [%]"] >= 0]
    print(f"LWC >= 0 AND RH >= 0: {len(filtered)}")
    filtered = filtered.loc[filtered["temp_amb [C]"] < 0]
    print(f"LWC >= 0 AND RH >= 0 and T <0 : {len(filtered)}")
    return filtered


flights = glob.glob("split/*/*/*/")

seed = []
for flight in flights:

    adc_fname = glob.glob(f"{flight}/*adc.csv")[0]
    fin_fname = glob.glob(f"{flight}/*fin.csv")[0]
    wind_fname = glob.glob(f"{flight}/*wind.csv")[0]

    fin = pd.read_csv(fin_fname, parse_dates=True, index_col="datetime")
    wind = pd.read_csv(wind_fname, parse_dates=True, index_col="datetime")
    adc = pd.read_csv(adc_fname, parse_dates=True, index_col="datetime")

    fin.index = fin.index.round("s")
    wind.index = wind.index = wind.index.round("s")

    fin = fin[~fin.index.duplicated(keep="first")]
    wind = wind[~wind.index.duplicated(keep="first")]

    merged = pd.concat([fin, wind], axis=1)

    # plot_3d_colorbar(lat, lon, alt, lwc)

    if (merged["seed-a [cnt]"].max() > 0) or (merged["seed-b [cnt]"].max() > 0):
        seed.append(merged)

seed_merged = pd.concat(seed)

summary = pd.read_csv("summary.csv")
# plot_bar(summary, "seed_total")
# plot_bar_stacked(summary, "seed_a", "seed_b")
# plot_bar(summary, "lwc_median")


seed_locations = seed_merged[
    (seed_merged["seed-a [cnt]"].diff() > 0)
    | (seed_merged["seed-b [cnt]"].diff() > 0)
]

seed_locations = filter_data(seed_locations)


# lat = seed_locations["lat [deg]"]
# lon = seed_locations["lon [deg]"]
# plot_scatter_map(seed_locations, "ss_total [%]")


# plot_hist(seed_locations, "ss_total [%]", filename="hist_ss_total_filtered.png")
# plot_hist(seed_locations, "ss_temp [%]")
# plot_hist(seed_locations, "ss_rh [%]")
# plot_hist(seed_locations, "ss_lwc [%]")
# plot_hist(seed_locations, "ss_updraft [%]")


slamfires = filter_slamfire(seed_locations, time_threshold=2)
print(*slamfires)

# plot_temp_ss_seed_ab(seed_merged)


dfs_by_date = [
    group for _, group in seed_locations.groupby(seed_locations.index.date)
]
# plot_scatter_gif(
#     dfs_by_date,
#     "ss_total [%]",
#     "Ambient Temperature (C)",
#     filename="temp_ss_scatter.gif",
# )


seed_merged_by_date = [
    group for _, group in seed_merged.groupby(seed_merged.index.date)
]


# for df in seed_merged_by_date:
#     plot_day_timeseries_with_seed_vlines(df, "temp_amb [C]")
# plot_day_timeseries_with_seed_vlines(df, "lwc [g/m^3]")
# plot_day_timeseries_with_seed_vlines(df, "gps_alt [m]")
# plot_day_timeseries_with_seed_vlines(df, "temp_amb [C]")

# for date in seed_merged_by_date:
#     last_column = date.iloc[:, -1]  # last column is named aircraft
#     seed_by_plane = [group for _, group in date.groupby(last_column)]
#     for plane in seed_by_plane:
#         seed_locations_before_seed = get_rows_before_seed(plane)
#         plot_flight_timeseries_with_seed_vlines(
#             plane, "lwc [g/m^3]", seed_locations_before_seed
#         )

# plot_flight_timeseries_with_seed_vlines(
#     plane, "wind_w [m/s]", seed_locations_before_seed
# )
# plot_flight_timeseries_with_seed_vlines(
#     plane, "rh [%]", seed_locations_before_seed
# )
# plot_flight_timeseries_with_seed_vlines(
#     plane, "ss_total [%]", seed_locations_before_seed
# )
# plot_flight_timeseries_with_seed_vlines(
#     plane, "temp_amb [C]", seed_locations_before_seed
# )
# x = "Ambient Temperature (C)"
# y = "temp_amb [C]"
# linregress_results = stats.linregress(plane[x], plane[y])
# plot_scatter(plane, x, y)


# plot_scatter(seed_locations, "ss_total [%]", "temp_amb [C]")
