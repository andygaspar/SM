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


sp = df["date"] == ldat
spa = df[sp]
len(spa)
ldat = lista_date[0]
def controllo_rip(dat,df = df):
    lista_critica = []
    indici = []
    cond = df["date"]==dat
    df_cp = df[cond] #considero solo una data
    i = 0
    while (i<df_cp.shape[0]):
        flight = df_cp.iloc[i]["aereo"]
        c_temp = df_cp["aereo"]==flight
        temp = df_cp[c_temp] #dataframe temporaneo con solo un aereo
        cont = 0
        #print(temp.shape[0])
        for j in range(temp.shape[0]):
            sid = temp.iloc[j]["sid"]
            if(sid=="KERAX" or sid =="PSA" or sid=="ROLIS" or sid=="UNOKO"):
                cont = cont + 1
        if(cont>=2):
            lista_critica.append(flight)
            indici.append(i)
        i += 1 + temp.shape[0]
        print(i)
    return lista_critica,indici

df_new = pd.DataFrame(columns = ["aereo","sid","coor","distance","date","time","time_sec"])

for i in range(len(a)):
    cond = df["aereo"]==a[i]
    temp = df[cond]
    df_new = df_new.append(temp)







"""
ddd=pd.read_csv("../data/punti_1709.csv")
ddd.iloc[180080:180110]
"""


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
