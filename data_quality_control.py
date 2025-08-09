import pandas as pd


def is_geolocated(df, col):
    count_diff = df[col].diff()
    time_diff = df.index.to_series().diff()
    has_lat = df["lat [deg]"].notna()
    has_lon = df["lon [deg]"].notna()
    return (
        (count_diff == 1)
        & (time_diff == pd.Timedelta(seconds=1))
        & has_lat
        & has_lon
    )
