import pandas as pd
import glob
from tqdm import tqdm
from readers import read_raw_data_parts


def format_timedelta(td):
    text = str(td)
    if text.startswith("0 days "):
        return text[7:]
    return text


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
    nan_rows = int(resampled_df.isna().all(axis=1).sum())
    nan_percentage = nan_rows / total_seconds * 100
    seed_a = len(
        df[df["seed-a [cnt]"].diff() > 0]
    )  # use this instead of .max()
    seed_b = len(df[df["seed-b [cnt]"].diff() > 0])
    seed_total = seed_a + seed_b
    summary = {
        "aircraft": aircraft,
        "start": first,
        "end": last,
        "duration": format_timedelta(duration),
        "total_seconds": total_seconds,
        "nan_rows": nan_rows,
        "nan_percentage": f"{nan_percentage:.1f}",
        "seed_a": seed_a,
        "seed_b": seed_b,
        "seed_total": seed_total,
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
