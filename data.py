import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun

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

def waypoint_per_volo(df):
    """
    dato un def (con waypoint non accorpati)
    ritorna un np array con il numero di waypoint per volo
    """
    waypoint_per_fl=[]
    j=0
    for i in range(df.shape[0]-1):
        if df.iloc[i]["ifps_id"]==df.iloc[i+1]["ifps_id"]:
            j+=1
        else:
            waypoint_per_fl.append(j)
            j=0
    return np.array(waypoint_per_fl)


"""
FUNZIONI ALBERTO PRESTA
"""
def aircraft_repetition(df,name_of_flight):
    dict = {}
    i=0
    while(i<df.shape[0]):
        aircraft = df.iloc[i][name_of_flight]
        cont = 1
        j =i
        while(j<df.shape[0]-2 and aircraft==df.iloc[j+1][name_of_flight]):
            cont=cont+1
            j=j+1
        dict[aircraft]=cont
        i=j+1
    return dict


def creation_data_waypoint(df,name,number_of_wp=5,name_of_col = "ifps_id"):
    """
    INPUT:
        -DataFrame
        -vettore con i nomi delle colonne del nuovo DataFrame
        -numero massimo_di_waypoint da considerare (per ora lo mettiamo)
    OUTPUT:
        -dataframe dove per ogni aereo viene associato il percorso degli
         ultimi "number_of_wp" waypints e i tempi
    """
    d = aircraft_repetition(df,name_of_col)

    df_traj=pd.DataFrame(columns=name)
    i = 0
    while(i<df.shape[0]-1):
        aereo = df.iloc[i][name_of_col]
        row = []

        row.append(aereo)
        for s in range(2*number_of_wp + 1):
            row.append('None')
        cont = 1  # numero di stack relative a questo aereoporto
        j = i #da cove iniziamo a contare
        while(j+1<df.shape[0] and cont<=number_of_wp-1 and aereo == df.iloc[j+1][name_of_col]):
            j = j+1 # andiamo avanti di un indice
            cont =cont+1 #contiamo gli stack
        if(cont<=number_of_wp):
            for k in range(cont):
                row[1+k] = df.iloc[i+cont-k-1]["sid"]
                row[1+k+number_of_wp]=df.iloc[i+cont-k-1]["time"]
            df_traj=df_traj.append(dict(zip(name,row)),ignore_index = True)
            i=j
            while (i<=df.shape[0]-2 and df.iloc[i][name_of_col]==df.iloc[i+1][name_of_col]):
                i+=1
            i+=1
        else:
            i=j
            i+=1
    return  df_traj


def arrival_matching(df_wp,df_arrivi,col_flights = "aereo"):
    """
    INPUT:
        -df_wp:datagrame dove per ogni volo ci sono tutti i waypoint con i rispettivi
         tempi-->voli relativi ad un unico giorno
         -df_arrivi_daframe dove per ogni volo c'è l'istante di arrivo-->voli relativi
          ad un solo giorno
         -nome della colonna relativa ai voli
    OUTPUT:
        -nuovo daframe con l'unione dei due precedenti
    """
    arrivi = []
    for i in range(df_wp.shape[0]):
        flight = df_wp.iloc[i][col_flights]
        cont = 0
        for j in range(df_arrivi.shape[0]):
            aereo = df_arrivi.iloc[j][col_flights]
            if(aereo==flight):
                cont = 1
                temp = df_arrivi.iloc[j]["time"]
                arrivi.append(temp)
        if(cont==0):
            arrivi.append("None")
    new_df = df_wp.copy()
    new_df["arrival"] = arrivi
    return new_df


def delete_useless_aircraft(df,cond):
    df = df[cond]
    return df
















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
