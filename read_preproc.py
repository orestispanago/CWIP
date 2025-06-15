import glob
import pandas as pd
from plotting import (
    plot_3d_colorbar,
    plot_hist,
    plot_scatter,
    plot_scatter_gif,
    plot_scatter_map,
    plot_temp_ss_seed_ab,
    plot_timeseries_with_seed_vlines,
    plot_bar,
)
import matplotlib.pyplot as plt


def calc_summary(df):
    aircraft = df["aircraft"].iloc[0].values[0]
    first = merged.index[0]
    last = merged.index[-1]
    duration = last - first
    numeric_cols = df.select_dtypes(include="number").columns
    string_cols = df.select_dtypes(exclude="number").columns

    # Resample numeric and string parts separately
    numeric_resampled = df[numeric_cols].resample("1s").mean()
    string_resampled = df[string_cols].resample("1s").first()  # or .last()
    # Combine them back
    resampled_df = pd.concat([numeric_resampled, string_resampled], axis=1)

    total_sec = len(resampled_df)
    nan_rows = int(resampled_df.isna().all(axis=1).sum())
    nan_percentage = nan_rows / total_sec * 100
    seed_a = len(resampled_df[resampled_df["seed-a [cnt]"].diff() > 0])
    seed_b = len(resampled_df[resampled_df["seed-b [cnt]"].diff() > 0])
    seed_total = seed_a + seed_b
    summary = {
        "aircraft": aircraft,
        "start": first,
        "end": last,
        "duration": duration,
        "total_seconds": total_sec,
        "nan_rows": nan_rows,
        "nan_percentage": nan_percentage,
        "seed_a": seed_a,
        "seed_b": seed_b,
        "seed_total": seed_total,
    }
    summary_df = pd.DataFrame([summary])
    return summary_df


flights = glob.glob("*/*/*/*/")

seed = []
summaries_list = []
for flight in flights:
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

    summary = calc_summary(merged)
    summaries_list.append(summary)
    # plot_3d_colorbar(lat, lon, alt, lwc)

    if (merged["seed-a [cnt]"].max() > 0) or (merged["seed-b [cnt]"].max() > 0):
        seed.append(merged)

seed_merged = pd.concat(seed)

summaries = pd.concat(summaries_list)
summaries.reset_index(drop=True, inplace=True)
summaries.to_csv("summaries.csv", index=False)

plot_bar(summaries, "seed_total")

# seed_merged = seed_merged[seed_merged["LWC (g/m^3)"] > 0]
# seed_merged = seed_merged[seed_merged["Ambient Temperature (C)"] < 0]


# seed_locations = seed_merged[
#     (seed_merged["seed-a [cnt]"].diff() > 0)
#     | (seed_merged["seed-b [cnt]"].diff() > 0)
# ]

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
# for df in seed_merged_by_date:

# plot_timeseries_with_seed_vlines(df, "Ambient Temperature (C)")
# plot_timeseries_with_seed_vlines(df, "LWC (g/m^3)")
# plot_timeseries_with_seed_vlines(df, "gps_alt [m]")
