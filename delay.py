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



#ddd=pd.read_csv("../data/punti_1709.csv")
#ddd.iloc[180080:180110]



def df_wp(df,wp,voli):
    """
    sotto fun di df_lista_wp
    seleziona i voli per wp e controllando che non siano nella lista voli e aggiorna la lista
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



    """
    sotto fun di df_finale

    lancia le iterazioni di df_wp, calcolando la prima e creando la relativa lista voli
    aggunge al df_new quello creato da df_wp
    """

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

    """
    dati df entrate e arrivi, una data, e una lista di wp
    ritorna un df con il tempo di arrivo e il flytime
    """
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
    """
    uguale a df dinale solo con l'aggiunta del delay
    ritorna df finale e un dict con i tempi minimi di percorrenza di ciascun wp
    """
    df_delay=df_finale(df,df_ar,date,lista_waypoint)
    delay_dict=fun.min_time_dict(df_delay,lista_waypoint)
    delay=np.zeros(df_delay.shape[0])
    for i in range(df_delay.shape[0]):
        delay[i]=df_delay.iloc[i]["fly time"]-delay_dict[df_delay.iloc[i]["sid"]]

    df_delay["delay"]=delay
    return df_delay,delay_dict



def sort_df(df):
    df_ordinato=df.sort_values(by="a_time_sec")
    delay=df_ordinato["delay"].values
    return df_ordinato,delay




"********************** programma ******************************"
l=["KERAX","PSA","ROLIS","UNOKO"]
d=lista_date[0]
df_uno,min_dict=df_finale_delay(df,df_ar,d,l)
df_tot,min_dict_tot=df_finale_delay(df,df_ar,d,lista_wp)

np.mean(delay)
plt.plot(delay/60,color="red")

p=plt.hist(df_ordinato["a_time_sec"].values,bins=24)
plt.show()



df_day1=data.df_per_data(df,lista_date[0])
df_day1.shape









num_fl=1
for i in range(df_day1.shape[0]-1):
    if df_day1.iloc[i]["aereo"]!=df_day1.iloc[i+1]["aereo"]:
        num_fl+=1
num_fl
