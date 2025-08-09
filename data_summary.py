import pandas as pd
import glob
from tqdm import tqdm
from data_readers import read_cwip_components
from data_quality_control import is_geolocated
from utils import resample_1s, select_cloud_penetrations

def format_timedelta(td):
    text = str(td)
    if text.startswith("0 days "):
        return text[7:]
    return text


def count_seed_events(df, col):
    df_not_na = df.dropna(subset=[col])
    seed_count_first = df_not_na[col].values[0]
    seed_count_last = df_not_na[col].values[-1]
    return seed_count_last - seed_count_first


def calc_summary(df, fname):
    aircraft = df["aircraft"].iloc[0].values[0]
    first = df.index[0]
    last = df.index[-1]
    duration = last - first  # it is not flight time or air time

    resampled_df = resample_1s(df)

    total_seconds = len(resampled_df)
    missing_seconds = int(resampled_df.isna().all(axis=1).sum())
    missing_seconds_percentage = missing_seconds / total_seconds * 100

    seed_a = count_seed_events(df, "seed-a [cnt]")
    seed_b = count_seed_events(df, "seed-b [cnt]")
    seed_total = seed_a + seed_b

    nan_coords = df[["lat [deg]", "lon [deg]"]].isna().any(axis=1).sum()
    nan_coords_percentage = nan_coords / len(df) * 100

    seed_a_loc = is_geolocated(df, "seed-a [cnt]").sum()
    seed_b_loc = is_geolocated(df, "seed-b [cnt]").sum()
    seed_loc_total = seed_a_loc + seed_b_loc

    seed_a_noloc = seed_a - seed_a_loc
    seed_b_noloc = seed_b - seed_b_loc
    seed_noloc_total = seed_a_noloc + seed_b_noloc
    
    penetrations02 = len(select_cloud_penetrations(df, lwc_threshold=0.2))
    penetrations025 = len(select_cloud_penetrations(df, lwc_threshold=0.25))
    penetrations03 = len(select_cloud_penetrations(df, lwc_threshold=0.3))
    penetrations035 = len(select_cloud_penetrations(df, lwc_threshold=0.35))
    penetrations04 = len(select_cloud_penetrations(df, lwc_threshold=0.4))

    summary = {
        "aircraft": aircraft,
        "start": first,
        "end": last,
        "duration": format_timedelta(duration),
        "total_seconds": total_seconds,
        "missing_seconds": missing_seconds,
        "missing_seconds_percentage": f"{missing_seconds_percentage:.2f}",
        "nan_coords": nan_coords,
        "nan_coords_percentage": f"{nan_coords_percentage:.2f}",
        "seed_a": seed_a,
        "seed_b": seed_b,
        "seed_total": seed_total,
        "seed_a_loc": seed_a_loc,
        "seed_b_loc": seed_b_loc,
        "seed_loc_total": seed_loc_total,
        "seed_a_noloc": seed_a_noloc,
        "seed_b_noloc": seed_b_noloc,
        "seed_noloc_total": seed_noloc_total,
        "penetrations02":penetrations02,
        "penetrations025":penetrations025,
        "penetrations03":penetrations03,
        "penetrations035":penetrations035,
        "penetrations04":penetrations04,
        "cwip_file": fname,
    }
    summary_df = pd.DataFrame([summary])
    return summary_df


files = glob.glob("KSA CWIP Files/**/*.csv", recursive=True)

summary_list = []
for fname in tqdm(files):
    adc, wind, fin, metadata_wide = read_cwip_components(fname, to_numeric=True)
    fin.index = fin.index.round("s")
    wind.index = wind.index.round("s")

    fin = fin[~fin.index.duplicated(keep="first")]
    wind = wind[~wind.index.duplicated(keep="first")]

    merged = pd.concat([fin, wind], axis=1)
    file_summary = calc_summary(merged, fname)
    summary_list.append(file_summary)

summary = pd.concat(summary_list)
summary.reset_index(drop=True, inplace=True)
summary = summary.sort_values("start")
summary.to_csv("summary.csv", index=False)
