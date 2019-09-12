import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data
import csv
import copy


df=pd.read_csv("../data/completo.csv")
df_ar=pd.read_csv("../data/arrivi_completo.csv")
df=data.dist_filter(df,200)
lista_date,lista_wp,lista_freq_wp=data.carica_liste()
lista_date
lista_wp
lista_freq_wp

df

"""
ddd=pd.read_csv("../data/punti_1709.csv")
ddd.iloc[180080:180110]
"""


def df_wp(df,wp,voli):
    """
    sotto fun di df_lista_wp
    """
    df_n=df.copy()
    cond=df_n["sid"]==wp
    df_n=df_n[cond]
    for volo in voli:
        cond=df_n["aereo"]!=volo
        df_n=df_n[cond]
    voli+=list(df_n["aereo"].values)
    return df_n,voli



def df_lista_wp(df,lista_wp):
    #primo volo

    df_new=df.copy()
    cond=df_new["sid"]==lista_wp[0]
    df_new=df_new[cond]
    voli=list(df_new["aereo"].values)
    lista_wp.pop(0)
    lista_wp

    #altri voli
    for wp in lista_wp:
        df_aux,voli=df_wp(df,wp,voli)
        df_new=df_new.append(df_aux.copy(),ignore_index=True)
    return df_new


def df_finale(df,df_ar,date,lista_waypoint):
    lista_wp=copy.deepcopy(lista_waypoint)
    df_day=data.df_per_data(df,date)
    df_new=df_lista_wp(df_day,lista_wp)
    a=[]
    ta=[]
    tv=[]
    for i in range(df_new.shape[0]):
        cond=df_ar["aereo"]==df_new.iloc[i]["aereo"]
        aux=df_ar[cond]
        a.append(aux["time"].values[0])
        ta.append(aux["time_sec"].values[0])
        tv.append(ta[i]-df_new.iloc[i]["time_sec"])

    df_new["a_time"]=a
    df_new["a_time_sec"]=ta
    df_new["fly time"]=tv

    return df_new

def df_finale_delay(df,df_ar,date,lista_waypoint):
    df_delay=df_finale(df,df_ar,date,lista_waypoint)
    delay_dict=fun.min_time_dict(df_delay,lista_waypoint)
    delay=np.zeros(df_delay.shape[0])
    for i in range(df_delay.shape[0]):
        delay[i]=df_delay.iloc[i]["fly time"]-delay_dict[df_delay.iloc[i]["sid"]]

    df_delay["delay"]=delay
    return df_delay,delay_dict


l=lista_wp[0:3]
d=lista_date[0]
l
df_uno,min_dict=df_finale_delay(df,df_ar,d,l)
df_uno
min_dict


df_ordinato=df_uno.sort_values(by="a_time_sec")
df_ordinato
delay=df_ordinato["delay"].values

np.mean(delay)
plt.plot(delay/60)
