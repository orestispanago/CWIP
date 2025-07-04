from tqdm import tqdm
import glob
import os
from readers import read_raw_data_parts


def create_dest_path(fname, output_dir):
    """Creates destination directory.
    Returns full destination path without extension."""
    base_name = os.path.basename(fname)
    stem = os.path.splitext(base_name)[0]
    date_time = stem.split("_")[-1]
    dir_name_parts = os.path.dirname(fname).split(os.sep)
    period = dir_name_parts[1]
    aircraft = dir_name_parts[2]
    dest_dir = f"{output_dir}/{period}/{aircraft}/{date_time}"
    os.makedirs(dest_dir, exist_ok=True)
    return f"{dest_dir}/cwip_{date_time}"


def parts_to_csv(fname, adc, wind, fin, metadata_wide, output_dir="split"):
    dest_path = create_dest_path(fname, output_dir)
    adc.to_csv(f"{dest_path}_adc.csv", index=True)
    wind.to_csv(f"{dest_path}_wind.csv", index=True)
    fin.to_csv(f"{dest_path}_fin.csv", index=True)
    metadata_wide.to_csv(f"{dest_path}_metadata.csv", index=False)


files = glob.glob("KSA CWIP Files/**/*.csv", recursive=True)

for fname in tqdm(files):
    adc, wind, fin, metadata_wide = read_raw_data_parts(fname)
    parts_to_csv(fname, adc, wind, fin, metadata_wide)
