import glob
import pandas as pd
from plotting import plot_scatter


flights = glob.glob("*/*/*/*/")


df_list = []
for flight in flights:

    adc_fname = glob.glob(f"{flight}/*adc.csv")[0]
    fin_fname = glob.glob(f"{flight}/*fin.csv")[0]
    wind_fname = glob.glob(f"{flight}/*wind.csv")[0]

    fin = pd.read_csv(fin_fname, parse_dates=True, index_col="datetime")
    wind = pd.read_csv(wind_fname, parse_dates=True, index_col="datetime")
    adc = pd.read_csv(adc_fname, parse_dates=True, index_col="datetime")

    fin.index = fin.index.round("s")
    wind.index = wind.index = wind.index.round("s")

    fin = fin[~fin.index.duplicated(keep="first")]
    wind = wind[~wind.index.duplicated(keep="first")]

    merged = pd.concat([fin, wind], axis=1)
    df_list.append(merged)

df_all = pd.concat(df_list)


plot_scatter(
    df_all,
    "lwc [g/m^3]",
    "lwc_dat [g/m^3]",
    filename="plots/reverse-engineering/scatter-lwc-lwc_dat.png",
)

plot_scatter(
    df_all,
    "temp_amb [C]",
    "ss_temp [%]",
    filename="plots/reverse-engineering/scatter-temp_amb-ss_temp.png",
)
plot_scatter(
    df_all,
    "rh [%]",
    "ss_rh [%]",
    filename="plots/reverse-engineering/scatter-rh-ss_rh.png",
)
plot_scatter(
    df_all,
    "lwc [g/m^3]",
    "ss_lwc [%]",
    filename="plots/reverse-engineering/scatter-lwc-ss_lwc.png",
)
plot_scatter(
    df_all,
    "wind_w [m/s]",
    "ss_updraft [%]",
    filename="plots/reverse-engineering/scatter-wind_w-ss_updraft.png",
)
