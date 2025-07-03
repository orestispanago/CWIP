import pandas as pd
import glob
from tqdm import tqdm
from readers import read_raw_data_parts
from quality_control import is_geolocated



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

    numeric_cols = df.select_dtypes(include="number").columns
    string_cols = df.select_dtypes(exclude="number").columns
    # Resample numeric and string parts separately
    numeric_resampled = df[numeric_cols].resample("1s").mean()
    string_resampled = df[string_cols].resample("1s").first()  # or .last()
    # Combine them back
    resampled_df = pd.concat([numeric_resampled, string_resampled], axis=1)

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
        "cwip_file": fname,
    }
    summary_df = pd.DataFrame([summary])
    return summary_df


files = glob.glob("KSA CWIP Files/**/*.csv", recursive=True)

summary_list = []
for fname in tqdm(files):
    adc, wind, fin, metadata_wide = read_raw_data_parts(fname, to_numeric=True)
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
