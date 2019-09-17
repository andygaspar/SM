import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data


def arr_hist(date,airport,BINS=24):
    """
    dato airport, data e numero bins  (BINS=default 24)
    stampa istogramma e ritorna l'array con gli arrivi
    """
    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.airport(df_ar,airport)
    arr_day=data.df_per_data(arr_day,date)
    arr_day=arr_day.sort_values(by="time_sec")
    arr_array=arr_day["time_sec"].values
    max_bin=max(arr_array)
    min_bin=min(arr_array)
    width_bin=(max_bin-min_bin)/BINS
    plt.hist(arr_array,bins=BINS, histtype='bar', ec='black')
    plt.xticks(np.arange(min_bin,max_bin, width_bin),range(0,23))
    plt.show()
    return arr_array


def freq_busy(start,end,date,airport):
    """
    dato ora iniziale, ora finale, data
    ritorna frequenza dei voli e df arrival con i voli nella fascia oraria
    """
    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.df_per_data(df_ar,date)
    arr_day=data.airport(arr_day,airport)
    #selezione in base al plot della fascia oraria le start-end
    cond=arr_day["time_sec"]>start*3600
    busy_arrival=arr_day[cond]
    cond=busy_arrival["time_sec"]<end*3600
    busy_arrival=busy_arrival[cond]

    #calcolo frequenza
    freq=(end-start)*3600/busy_arrival.shape[0]
    return freq,busy_arrival


"""
#distribuzione frequenza nelle ore della giornata





#selezione in base al plot della fascia oraria le 5-21
len(arrival)
cond=arrival>5*3600
busy_arrival=arrival[cond]
len(busy_arrival)
cond=busy_arrival<21*3600
busy_arrival=busy_arrival[cond]
len(busy_arrival)
sec_to_time(busy_arrival[-1])



#calcolo frequenza
freq=(21-5)*3600/len(busy_arrival)
freq
"""




"""
problemino, il numero di arrival è inferiore al numero di aerei nel completo


date='2017-08-27'
df=pd.read_csv("../data/completo.csv")
df=data.df_per_data(df,date)
count=1
for i in range(df.shape[0]-1):
    if df.iloc[i]["aereo"]!=df.iloc[i+1]["aereo"]:
        count+=1
count
df_ar=pd.read_csv("../data/arrivi_completo.csv")
arr_day=data.df_per_data(df_ar,date)
arr_day.shape[0]


"""
