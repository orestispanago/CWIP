import glob
import pandas as pd
import tqdm
import numpy as np
import os


files = glob.glob("KSA CWIP Files/**/*.csv", recursive=True)
datetime_fmt = "%Y_%m_%d_%H_%M_%S.%f"


def get_header(fname, row=26):
    header = pd.read_csv(fname, header=None, skiprows=row, nrows=1, sep=",")
    header = header.dropna(axis=1)
    header_list = header.values[0]
    header_list = np.insert(header_list, 0, "datetime")
    return header_list


first_file = files[0]

fin_header = get_header(first_file, row=26)
adc_header = get_header(first_file, row=28)
wind_header = get_header(first_file, row=29)

for fname in tqdm.tqdm(files):
    adc_rows = []
    wind_rows = []
    fin_rows = []

    dir_name = os.path.dirname(fname).split(os.sep)
    aircraft = dir_name[-1]
    period = dir_name[-2]
    with open(fname, "r") as f:
        for line in f:
            line = line.strip().split(",")
            if "$ADC1" in line:
                adc_rows.append(line)
            if "$CWIP_WIND" in line:
                wind_rows.append(line)
            if "$Fin-2" in line:
                fin_rows.append(line)

    adc_df = pd.DataFrame(adc_rows)
    adc_df.columns = adc_header
    adc_df["datetime"] = pd.to_datetime(adc_df["datetime"], format=datetime_fmt)
    adc_df.set_index("datetime", inplace=True)
    adc_df["aircraft"] = aircraft

    wind_df = pd.DataFrame(wind_rows)
    wind_df = wind_df.loc[:, :49]  # Removing last 2 unnamed columns
    wind_df.columns = wind_header
    wind_df.index = pd.to_datetime(wind_df.datetime, format=datetime_fmt)
    wind_df["datetime"] = pd.to_datetime(
        wind_df["datetime"], format=datetime_fmt
    )
    wind_df.set_index("datetime", inplace=True)
    wind_df["aircraft"] = aircraft

    fin_df = pd.DataFrame(fin_rows)
    fin_df = fin_df.dropna(axis=1, how="all")
    fin_df = fin_df.loc[:, :67]  # Removing last 1 unnamed column
    fin_df.columns = fin_header
    fin_df["datetime"] = pd.to_datetime(
        fin_df["datetime"], format=datetime_fmt
    ).dt.floor("s")
    fin_df.set_index("datetime", inplace=True)
    fin_df["aircraft"] = aircraft

    base_name = os.path.basename(fname)
    stem = os.path.splitext(base_name)[0]
    date_time = stem.split("_")[-1]

    dest_dir = f"preproc/{period}/{aircraft}/{date_time}"
    os.makedirs(dest_dir, exist_ok=True)
    adc_df.to_csv(f"{dest_dir}/{stem}_adc.csv", index=True)
    wind_df.to_csv(f"{dest_dir}/{stem}_wind.csv", index=True)
    fin_df.to_csv(f"{dest_dir}/{stem}_fin.csv", index=True)
