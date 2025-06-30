import pandas as pd


def read_col_names(fname, row=26):
    header = pd.read_csv(fname, header=None, skiprows=row, nrows=1, sep=",")
    header = header.dropna(axis=1)
    header_list = header.values[0]
    return header_list


def read_metadata_partial(fname):
    df1 = pd.read_csv(fname, header=None, nrows=4, sep=":")
    df2 = pd.read_csv(fname, header=None, skiprows=20, nrows=5, sep=",")
    metadata = pd.concat([df1, df2])
    metadata.reset_index(drop=True, inplace=True)
    return metadata


def read_cal_params(fname):
    cal_params = pd.read_csv(fname, header=None, skiprows=4, nrows=16, sep=",")
    cal_params[0] = cal_params[0].str.replace(" Cal Params", "")
    return cal_params


def cols_to_numeric(df, exclude_cols=[]):
    for i, col in enumerate(df.columns):
        if i not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")


def datetime_col_to_index(df):
    df[0] = pd.to_datetime(df[0], format="%Y_%m_%d_%H_%M_%S.%f")
    df.set_index(0, inplace=True)
    df.index.name = "datetime"


def select_adc(df, header, to_numeric):
    adc = df[df[1] == "$ADC1"]
    adc = adc.iloc[:, : len(header) + 1]
    if to_numeric:
        cols_to_numeric(adc, exclude_cols=[0, 1, 5, 6, len(header)])
    datetime_col_to_index(adc)
    adc.columns = header
    return adc


def select_fin(df, header, to_numeric):
    fin = df[df[1] == "$Fin-2"]
    fin = fin.iloc[:, : len(header) + 1]
    if to_numeric:
        cols_to_numeric(fin, exclude_cols=[0, 1])
    datetime_col_to_index(fin)
    fin.columns = header
    return fin


def select_wind(df, header, to_numeric):
    wind = df[df[1] == "$CWIP_WIND"]
    wind = wind.iloc[:, : len(header) + 1]
    if to_numeric:
        cols_to_numeric(wind, exclude_cols=[0, 1])
    datetime_col_to_index(wind)
    wind.columns = header
    return wind


def widden_cal_params(df):
    wide_dict = {}
    for row in df.itertuples(index=False):
        base_name = row[0]
        for count, value in enumerate(row[1:], start=1):
            wide_dict[f"{base_name} {count}"] = value
    df_wide = pd.DataFrame([wide_dict])
    return df_wide


def read_raw_data_parts(fname, to_numeric=False):
    raw_data = pd.read_csv(
        fname, header=None, names=list(range(69)), low_memory=False
    )

    adc_header = read_col_names(fname, row=28)
    adc = select_adc(raw_data, adc_header, to_numeric)

    fin_header = read_col_names(fname, row=26)
    fin = select_fin(raw_data, fin_header, to_numeric)

    wind_header = read_col_names(fname, row=29)
    wind = select_wind(raw_data, wind_header, to_numeric)

    metadata_partial = read_metadata_partial(fname)
    metadata_partial_wide = metadata_partial.set_index(0).T.reset_index(
        drop=True
    )

    cal_params = read_cal_params(fname)
    cal_params_wide = widden_cal_params(cal_params)

    metadata_wide = pd.concat([metadata_partial_wide, cal_params_wide], axis=1)

    aircraft = metadata_wide["AircraftID"].values[0]
    for df in [adc, fin, wind]:
        df["aircraft"] = aircraft
    return adc, wind, fin, metadata_wide
