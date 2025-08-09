import pandas as pd


def select_time_windows(df, center_times, window_timedelta):
    time_windows = []
    for count, time in enumerate(center_times.index):
        start = time - window_timedelta / 2
        end = time + window_timedelta / 2
        time_window = df[start:end].copy()
        time_window["window_count"] = count
        if not time_window.empty:
            time_windows.append(time_window)
    return time_windows


def time_windows_to_df(time_windows):
    time_windows_list = []
    for count, time_window in enumerate(time_windows):
        time_window_c = time_window.copy()
        time_windows_list.append(time_window_c)
    return pd.concat(time_windows_list)


def to_relative_time_index(df):
    """Returns a new DataFrame with the index converted to relative seconds
    from the center timestamp, corresponding to the seed event."""
    df_rel = df.copy()
    center_time = df_rel.index[len(df_rel) // 2]
    df_rel["relative_time"] = (
        (df_rel.index - center_time).total_seconds().astype(int)
    )
    df_rel = df_rel.set_index("relative_time")
    return df_rel
