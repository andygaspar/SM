import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import csv

#CIAO

df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")



def save_df(df,name):
    """
    dato un df e un path/name
    salva il DataFrame
    """
    export_csv = df.to_csv (name, index = None, header=True)



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
        kk=kk.split()
        date.append(kk[0])
        landing.append(kk[1])
    df["date"]=date
    df["time"]=landing
    df.drop(columns=[label])
    return df


def add_time_in_sec(df):
    """
    dato un df con la colonna time
    agggiunge la colonna time_sec con il tempo numerico (int)
    """
    time_sec=[]
    for i in range(df.shape[0]):
        time_sec.append(fun.time_to_sec(df.iloc[i]["time"]))
    df["time_sec"]=time_sec


def taglio_colonne(df,lista):
    """
    dato un df, data la llista delle colonne da eliminare
    ritorna un df con le colonne eliminate
    """
    df.drop(columns=lista,inplace=True)



def crea_completo():
    df_wp=pd.read_csv("../data/punti_1709.csv")
    df=df_wp.copy()
    data.rinomina(df,3,"coor")
    data.rinomina(df,4,"sid")
    data.rinomina(df,5,"aereo")
    da_togliere=["trajectory_id","geopoint_id","ac_id","D","O"]
    data.taglio_colonne(df,da_togliere)
    df=df[["aereo","sid","coor","distance","time_over"]]
    data.add_dist(df)
    data.data_time(df)
    data.taglio_colonne(df,["time_over"])
    data.add_time_in_sec(df)
    df=df[~df.duplicated()]
    return df

def crea_completo_filtrato(df):
    df_new=df.copy()
    df_new=data.dist_filter(df,200)
    return df_new



def crea_arrivi():
    df_ar=pd.read_csv("../data/arrivi_1709.csv")
    da_togliere=["ac_id","D","O"]
    df_ar=data.taglio_colonne(df_ar,da_togliere)
    data.data_time(df_ar,"arr_time")
    df_ar=data.taglio_colonne(df_ar,["arr_time"])
    data.rinomina(df_ar,"ifps_id","aereo")
    add_time_in_sec(df_ar)
    return df_ar




def carica_liste():
    lista_date=[]
    with open('../data/lista_date.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            lista_date.append(row)

    wp=[]
    with open('../data/lista_wp.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            wp.append(row)

    freq_wp=[]
    with open('../data/lista_freq_wp.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            freq_wp.append(row)
    freq_wp=freq_wp[0]
    for i in range(len(freq_wp)):
        freq_wp[i]=int(freq_wp[i])

    return lista_date[0],wp[0],freq_wp




def df_per_data(df,date):
    entry_condition=df['date']==date
    return df[entry_condition]
