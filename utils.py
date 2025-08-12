import pandas as pd


def resample_1s(df):
    numeric_cols = df.select_dtypes(include="number").columns
    string_cols = df.select_dtypes(exclude="number").columns
    # Resample numeric and string parts separately
    numeric_resampled = df[numeric_cols].resample("1s").mean()
    string_resampled = df[string_cols].resample("1s").first()  # or .last()
    # Combine them back
    return pd.concat([numeric_resampled, string_resampled], axis=1)


def select_seed_locations(df):
    return df[
        (df["seed-a [cnt]"].diff() > 0) | (df["seed-b [cnt]"].diff() > 0)
    ].copy()


def select_cloud_penetrations(df, lwc_threshold=0.3):
    return df[df["lwc [g/m^3]"].diff() > lwc_threshold].copy()

def get_index_middle(df):
    return df.index[(len(df.index) - 1) // 2]