import pandas as pd
import glob
from config import SPLIT_DATA

metadata_files = glob.glob(f"{SPLIT_DATA}/**/*metadata.csv", recursive=True)

metadata_list = []
for f in metadata_files:
    df = pd.read_csv(f)
    metadata_list.append(df)

metadata = pd.concat(metadata_list, ignore_index=True)

metadata_by_plane = [group for _, group in metadata.groupby("AircraftID")]


for df in metadata_by_plane:
    print(df["AircraftID"].values[0])
    print("---------------------")
    for col in list(df):
        print(col, df[col].unique())
    print("---------------------")
