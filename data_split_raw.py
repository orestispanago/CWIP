from tqdm import tqdm
import glob
import os
from data_readers import read_cwip_components


def create_dest_path(fname, output_dir, period, aircraft):
    """Creates destination directory.
    Returns full destination path without extension."""
    base_name = os.path.basename(fname)
    stem = os.path.splitext(base_name)[0]
    date_time = stem.split("_")[-1]
    dest_dir = f"{output_dir}/{period}/{aircraft}/{date_time}"
    os.makedirs(dest_dir, exist_ok=True)
    return f"{dest_dir}/cwip_{aircraft}_{date_time}"


def parts_to_csv(fname, adc, wind, fin, metadata_wide, output_dir="data/split"):
    period = wind["period"].values[0]
    aircraft = wind["aircraft"].values[0]
    dest_path = create_dest_path(fname, output_dir, period, aircraft)
    adc.to_csv(f"{dest_path}_adc.csv", index=True)
    wind.to_csv(f"{dest_path}_wind.csv", index=True)
    fin.to_csv(f"{dest_path}_fin.csv", index=True)
    metadata_wide.to_csv(f"{dest_path}_metadata.csv", index=False)


files = glob.glob("data/KSA CWIP Files/**/*.csv", recursive=True)

for fname in tqdm(files):
    adc, wind, fin, metadata_wide = read_cwip_components(fname)
    aircraft = metadata_wide["AircraftID"].values[0].strip()
    period = os.path.dirname(fname).split(os.sep)[2]
    for df in [adc, fin, wind]:
        df["aircraft"] = aircraft
        df["period"] = period
    parts_to_csv(fname, adc, wind, fin, metadata_wide)
