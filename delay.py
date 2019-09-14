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
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()
df=data.df_per_data(df,lista_date[0])



lista_date
lista_wp
lista_freq_wp
d_wp_coor
df



#ddd=pd.read_csv("../data/punti_1709.csv")
#ddd.iloc[180080:180110]



def df_lista_wp(df,lista_wp):

    """
    sotto fun di df_finale

    lancia le iterazioni di df_wp, calcolando la prima e creando la relativa lista voli
    aggunge al df_new quello creato da df_wp
    """
    df_new = pd.DataFrame(data=None, columns=df.columns)
    voli=[]
    for i in range(df.shape[0]):
        if df.iloc[i]["sid"] in lista_wp and df.iloc[i]["aereo"] not in voli:
            df_new=df_new.append(df.iloc[i].copy(),ignore_index=True)
            voli.append(df.iloc[i]["aereo"])
    return df_new


def df_finale(df,df_ar,date,lista_waypoint):

    """
    dati df entrate e arrivi, una data, e una lista di wp
    ritorna un df con il tempo di arrivo e il flytime
    """
    df_day=data.df_per_data(df,date)
    df_new=df_lista_wp(df_day,lista_waypoint)
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
#df_tot,min_dict_tot=df_finale_delay(df,df_ar,d,lista_wp)
min_dict
df_uno

df_uno,delay=sort_df(df_uno)
df_uno

df_uno.iloc[np.argmax(delay)]["aereo"]

plt.plot(delay/60,color="red")

p=plt.hist(df_ordinato["a_time_sec"].values,bins=24)
plt.show()

cond=df["aereo"]==df_uno.iloc[np.argmax(delay)]["aereo"]
df_max_delay=df[cond]

df


df_max_delay
AA67325474
AA67325474

df_base=pd.read_csv("../data/punti_1709.csv")
dd=pd.read_csv("../data/completo.csv")
dd.shape
df_base.shape
cond=df_base['ifps_id']==df_uno.iloc[np.argmax(delay)]["aereo"]
df_max_delay_base=df_base[cond]
df_max_delay_base



def print_trajectory()
