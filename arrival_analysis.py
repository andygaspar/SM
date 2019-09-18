import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data


def arr_hist(date,airport,index=0,BINS=24):
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
    plt.title(airport+" "+date+" "+str(index))
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
    cond=arr_day["time_sec"]>=start*3600
    busy_arrival=arr_day[cond]
    cond=busy_arrival["time_sec"]<end*3600
    busy_arrival=busy_arrival[cond]

    #calcolo frequenza
    freq=(end-start)*3600/busy_arrival.shape[0]
    return freq,busy_arrival



#distribuzione frequenza nelle ore della giornata
def freq_analysis(date,airport,DEG=30):
    """
    data una data e un aeroporto
    restituisce:
        un vettore con tutte le frequenze inter arrival
        un vettore con le frequenze medie per ora
        un vettore con la curva che approx l'andamento della frequenza
            mediande i minimi quadrati con un pol di ordine DEG=30
    """

    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.df_per_data(df_ar,date)
    arr_day=data.airport(arr_day,airport)
    arr_day=arr_day.sort_values(by="time_sec")

    curve=np.zeros(arr_day.shape[0]-1)

    for i in range(arr_day.shape[0]-1):
        curve[i]=arr_day.iloc[i+1]["time_sec"]-arr_day.iloc[i]["time_sec"]


    freq_per_h=np.zeros(24)
    j=0
    for i in range(24):
        k=j
        while k<arr_day.shape[0] and arr_day.iloc[k]["time_sec"]<(i+1)*3600:
            k+=1
        if k>j+1:
            freq_per_h[i]=np.mean(curve[j:k+1])
        j=k

    pol=np.polyfit(arr_day["time_sec"].values[0:-1],curve,DEG)
    approx=np.polyval(pol,arr_day["time_sec"].values[0:-1])

    return curve, freq_per_h, approx




"""
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
