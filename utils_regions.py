import numpy as np


class SeparatorLine:
    def __init__(self, x1=39, y1=25, x2=48, y2=20):
        self.start = (x1, y1)
        self.end = (x2, y2)
        self.lons = [x1, x2]
        self.lats = [y1, y2]
        self.slope = (y2 - y1) / (x2 - x1)
        self.intercept = y1 - self.slope * x1


def classify_regions(df, sep_slope, sep_intercept):
    df["region"] = np.where(
        df["lat [deg]"] > sep_slope * df["lon [deg]"] + sep_intercept,
        "Central",
        "SW",
    )
    return df
