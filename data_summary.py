import pandas as pd
import glob
from tqdm import tqdm
from data_readers import read_wind_csv
from utils_summary import calc_summary

wind_files = glob.glob("split/**/*wind.csv", recursive=True)

summary_list = []
for fname in tqdm(wind_files):
    wind = read_wind_csv(fname)
    file_summary = calc_summary(wind, fname)
    summary_list.append(file_summary)

summary = pd.concat(summary_list)
summary.reset_index(drop=True, inplace=True)
summary = summary.sort_values("date")
summary.to_csv("summary.csv", index=False)
