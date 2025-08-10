import pandas as pd
from utils import resample_1s, select_cloud_penetrations
from data_quality_control import is_geolocated


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
    period = df["period"].iloc[0]
    aircraft = df["aircraft"].iloc[0].strip()
    
    start = df.index[0]
    end = df.index[-1]
    start_time = start.time()
    end_time = end.time()
    
    date = start.date()
    
    duration = end - start  # it is not flight time or air time

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
        "period": period,
        "aircraft": aircraft,
        "date":date,
        "start": start_time,
        "end": end_time,
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