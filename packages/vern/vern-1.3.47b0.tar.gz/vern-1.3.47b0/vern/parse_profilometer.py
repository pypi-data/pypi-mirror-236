# profilometer
import numpy as np
import pandas as pd
from .misc import *
__all__ = ['parse_profilometer']

def read_files(input_path, csv_path, plot_path, angle_plot_path, hist_path, interactive=False):
    with open(input_path, "r") as f:
        lines = f.readlines()

    df = pd_read_csv( 
        filename=input_path, encoding="utf-8", sep=", ", header_count=0,
        names_old=["position (mm)", "height (μm)"], names_new=["position (μm)", "height (nm)"], unit_conversion_coefficients=[1, 1],
    )
    df.to_csv(csv_path, index=False)
    set_min_0(df)
    df = remove_outlier(df)
    p = Plot(df, interactive=interactive)
    p.plot(plot_path)
    p.hist(hist_path)

    df_angle = pd.DataFrame()
    df_angle["position (μm)"] = df["position (μm)"][:-1]
    y = df["height (nm)"]
    dy = y[1:] - y[:-1]
    x = df["position (μm)"]*1000 # um -> nm
    dx = x[1:] - x[:-1]
    df_angle["angle (deg)"] = np.arctan2(dy, dx)*180/np.pi
    p = Plot(df_angle, interactive=interactive)
    p.plot(angle_plot_path)

def parse_profilometer(**kwargs):
    if "interactive" in kwargs.keys():
        interactive = kwargs["interactive"]
    else:
        interactive = False
    read_files(kwargs["input_path"], kwargs["csv_path"], kwargs["plot_path"], kwargs["angle_plot_path"], kwargs["hist_path"], interactive=interactive)