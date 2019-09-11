import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data



def sec_to_time(x):
    sec=x%60
    x-=sec
    min=int(x/60)%60
    x-=min
    h=int(x/3600)
    return str(h)+":"+str(min)+":"+str(sec)

df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")



data.data_time(df_ar,"arr_time")
data.data_time(df_wp)

cond=df_ar["date"]==df_ar.iloc[0]["date"]
cond

data.add_time_in_sec(df_ar)
sec_to_time(df_ar.iloc[0]["time_sec"])
