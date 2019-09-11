import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun

#CIAO

df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")


def rinomina(df,vecchio_nome_o_indice,nuovo_nome):
    """
    dato un df, un nome o l'indice del nome
    cambia il nome inplace
    """
    if type(vecchio_nome_o_indice)==str:
        return df.rename(columns={vecchio_nome_o_indice:nuovo_nome},inplace=True)
        return df_new
    else:
        i=vecchio_nome_o_indice
        return df.rename(columns={df.columns[i]:nuovo_nome},inplace=True)



def add_dist(df):
    """
    IL DF DEVE AVERE LA COLONNA "coor"
    aggiunge la colonna distanza al df
    """
    dist=fun.df_coor_to_dist(df)
    df["distance"]=dist



def dist_filter(df,dist):
    """
    dato un df MUNITO DELLA CLONNA DISTANZA, e una distanza
    ritorna un dataset con solo le righe taliche df["distanza"]<dist
    """
    #limitazione agli waypoint più vicini di 200km dall'aeroporto
    entry_condition=df['distance']<dist
    return df[entry_condition]

def add_time_in_sec(df):
    """
    dato un df con la colonna time
    agggiunge la colonna time_sec con il tempo numerico (int)
    """
    time_sec=[]
    for i in range(df.shape[0]):
        time_sec.append(fun.time_to_sec(df.iloc[i]["time"]))
    df["time_sec"]=time_sec


def save_df(df,name):
    """
    dato un df e un path/name
    salva il DataFrame
    """
    export_csv = df.to_csv (name, index = None, header=True)



def data_time(df,label="time_over"):
    """
    dato un df, data la label della colonna time
    crea un df con data e time separati e cancella la colonna time_over
    """
    #aggiunta colonna "data volo" e rimpiazzo colonna touch down con "time"
    date=[]
    landing=[]
    for i in range(df.shape[0]):
        kk=df.iloc[i][label]
        kk=kk.split(" ")
        date.append(kk[0])
        landing.append(kk[1])
    df["date"]=date
    df["time"]=landing
    df.drop(columns=[label])
    return df


def taglio_colonne(df,lista):
    """
    dato un df, data la llista delle colonne da eliminare
    ritorna un df con le colonne eliminate
    """
    return df.drop(columns=lista)

















def fun_da_eliminre_o_sistemare():
    pass
"""
aggiunta funzioni sul contteggio degli waypoint

è una lista con 5 dizionari ogniuno riferito ad
un wp, ordinati per numero di passaggi

    wp_dict_1={}
    wp_dict_2={}
    wp_dict_3={}
    wp_dict_4={}
    wp_dict_5={}
    stat_waypoint=[wp_dict_1,wp_dict_2,wp_dict_3,wp_dict_4,wp_dict_5]


    names=["wp1","wp2","wp3","wp4","wp5"]
    for j in range(5):
        for i in range(df_traj.shape[0]):
            way_p=df_traj.iloc[i][names[j]]
            if way_p in stat_waypoint[j]:
                stat_waypoint[j][way_p]+=1
            else:
                stat_waypoint[j][way_p]=1

        #riordino dizionario
        stat_waypoint[j]=sorted(stat_waypoint[j].items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
        stat_waypoint[j]=dict(stat_waypoint[j])
    stat_waypoint[0]
    'REDNI' in stat_waypoint[0]

    """
