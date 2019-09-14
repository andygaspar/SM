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


def sort_df(df,BY="a_time_sec"):
    """
    dato df e label
    ordina il df in base alla label
    """
    df_ordinato=df.sort_values(by=BY)
    delay=df_ordinato["delay"].values
    return df_ordinato,delay


def taglio_colonne(df,lista):
    """
    dato un df, data la llista delle colonne da eliminare
    ritorna un df con le colonne eliminate
    """
    df.drop(columns=lista,inplace=True)


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


def crea_completo():
    """
    crea completo dal row csv con tutti gli items
    """
    df_wp=pd.read_csv("../data/punti_1709.csv")
    df=df_wp.copy()
    rinomina(df,3,"coor")
    rinomina(df,4,"sid")
    rinomina(df,5,"aereo")
    da_togliere=["trajectory_id","geopoint_id","ac_id","D","O"]
    taglio_colonne(df,da_togliere)
    df=df[["aereo","sid","coor","distance","time_over"]]
    add_dist(df)
    data_time(df)
    taglio_colonne(df,["time_over"])
    add_time_in_sec(df)
    df=df[~df.duplicated()]
    return df


def crea_arrivi():
    """
    crea df arrivi pulito e con day e time separati e arrivo in sec
    """
    df_ar=pd.read_csv("../data/arrivi_1709.csv")
    da_togliere=["ac_id","D","O"]
    df_ar=taglio_colonne(df_ar,da_togliere)
    data_time(df_ar,"arr_time")
    df_ar=taglio_colonne(df_ar,["arr_time"])
    rinomina(df_ar,"ifps_id","aereo")
    add_time_in_sec(df_ar)
    return df_ar


def carica_liste():
    """
    carica 4 liste:
    lista date,lista wp ,frequenza wp, lista coordinate wp
    """
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

    wp_coordinate=[]
    with open('../data/wp_coor.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            wp_coordinate.append(row)


    return lista_date[0],wp[0],freq_wp,wp_coordinate


def df_per_data(df,date):
    """
    dato df e data
    crea df con solo i voli in quella data
    """
    entry_condition=df['date']==date
    return df[entry_condition]


def df_busy(df,start,end):
    """
    dato df_finale_delay, ora iniziale, ora finale
    df_finale_arrival con i voli nella fascia oraria
    """
    df_new=df.copy()
    #selezione in base al plot della fascia oraria le start-end
    cond=df["time_sec"]>start*3600
    busy_arrival=df[cond]
    cond=busy_arrival["time_sec"]<end*3600
    busy_arrival=busy_arrival[cond]

    return busy_arrival



def df_lista_wp(df,lista_wp):

    """
    sotto fun di df_finale

    dato df e lista
    crea df con il primo passaggio in uno dei pinti della lista
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
    dati df entrate e df arrivi, una data, e una lista di wp
    ritorna un df con solo un aereo per riga,
    con il suo primo passaggio per uno dei wp nella lista,
    in aggiunta il tempo di arrivo e il flytime
    """
    df_day=df_per_data(df,date)
    df_new=df_lista_wp(df_day,lista_waypoint)
    a=[]
    ta=[]
    tv=[]
    #aggiiunge tempo arrivo, tempo arrivo in sec, flytime
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
    uguale a df finale solo con l'aggiunta del delay
    ritorna un df e un dict con i tempi minimi di percorrenza di ciascun wp
    """
    df_delay=df_finale(df,df_ar,date,lista_waypoint)
    delay_dict=fun.min_time_dict(df_delay,lista_waypoint)
    delay=np.zeros(df_delay.shape[0])
    for i in range(df_delay.shape[0]):
        delay[i]=df_delay.iloc[i]["fly time"]-delay_dict[df_delay.iloc[i]["sid"]]

    df_delay["delay"]=delay
    return df_delay,delay_dict
