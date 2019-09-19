import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data
import csv
import copy

lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()



df=pd.read_csv("../data/completo.csv") # DA AGGIUNGERE : matcho con arrivo l'aereo con sid aereoporto
df_ar = pd.read_csv("../data/arrivi_1709.csv")
main=["KERAX","PSA","ROLIS","UNOKO"]
lista = ["aereo","sid","coor","distance","date","time","time_sec"]


def pre_processing_wp(df = df):
    df=data.dist_filter(df,200)
    df=data.df_per_data(df,'2017-08-17')
    return df


def pre_processing_arr(df=df_ar):
    df_ar = df.copy()
    data.rinomina(df_ar,"ifps_id","aereo")
    data.rinomina(df_ar,"ac_id","sid")
    data.data_time(df_ar,"arr_time")
    fr_cond = df_ar["D"] =="EDDF"
    df_ar = df_ar[fr_cond]
    for i in range(df_ar.shape[0]):
        df_ar.iloc[i]["sid"] = "AIRPORT"
    tempi = []
    for i in range(df_ar.shape[0]):
         t = df_ar.iloc[i]["time"]
         p = fun.time_to_sec(t)
         tempi.append(p)
    df_ar["time_sec"]=tempi
    df_ar["coor"]="POINT(50.037753 8.560964)"
    df_ar["distance"]=0
    df_ar = df_ar.drop(["O"],axis=1)
    df_ar = df_ar.drop(["arr_time"],axis=1)
    return df_ar


df = pre_processing_wp()
df_ar = pre_processing_arr()












def complete_dataframe(df = df,df_ar = df_ar, lista = lista):
    """
    INPUT : come input ci voglione due dataframe, il primo relativo ai passaggi nei
        waypoints, metre il secondo relativo agli arrivi
        il terzo input è una lista con i nomi delle colonne dei due dataframe, che ripeto
        DEVONO ESSERE UGUALI
    ATTENZIONE: siccome questa funzione si basa su appendere diversi dataframe,
                questi due devono avere le stesse colonne con lo stesso nome e lo stesso
                numero...questo comporta che prima il dataframe relativo agli arrivi
                debba essere modificato in tal senso
    OUTPUT: dataframe del percorso completo
    """
    #fase 1--> creare dict con tutti i voli e indice realtivo al daframe df
    df_totale = pd.DataFrame(columns = ["aereo","sid","coor","distance","date","time","time_sec"])
    pr = {}
    i = 0
    while(i<df.shape[0]):
        aer = df.iloc[i]["aereo"] #salvato l'aereo
        pr[aer] = i
        j=i+1
        while(j<df.shape[0]-1 and df.iloc[j]["aereo"]==aer ):
            j = j+1
        i = j
    lista_indici = list(pr.values())
    #fase due quello che dobbiamo fare
    for voli in pr:
        cond = df["aereo"]==voli
        temp = df[cond]
        #ora lavoro sui daframe temp
        cond_ar = df_ar["aereo"]==voli
        temp_arrival = df_ar[cond_ar]
        temp = temp.append(temp_arrival)
        df_totale = df_totale.append(temp)
    return df_totale


df_tot = complete_dataframe()
df_tot
def traiettorie_complete(df):
    """
        INPUT:
              -dataframe con notizie traiettorie_complete
        OUTPUT:
            -lista di liste delle traiettorie
    """
    aereo = df.iloc[0]["aereo"]
    traj_list = [[df.iloc[0]["sid"]]]
    j = 0
    for i in range(1,df.shape[0]):
        if aereo == df.iloc[i]["aereo"]:
            traj_list[j].append(df.iloc[i]["sid"])
        else:
            aereo = df.iloc[i]["aereo"]
            traj_list.append([df.iloc[i]["sid"]])
            j+=1
    return traj_list
trajectory=traiettorie_complete(df_tot)






"""
CREAZIONE WP_COORD
"""


def dict_coordinate(df = df):
    """
    INPUT: dataframe con informazioni sui voli
    OUTPUT: dizionario dove per ogni waypoint vengono associate le coordinate
            come liste e non come dict
    """
    wp_coord = {}
    for i in range(df.shape[0]):
        s = df.iloc[i]["sid"]
        coor = df.iloc[i]["coor"]
        coor = coor.replace("POINT","")
        coor = coor.replace("(","")
        coor = coor.replace(")","")
        coor = coor.split(" ")
        if(s not in wp_coord):
            wp_coord[s]=coor
    center = ["50.037753","8.560964"]
    wp_coord["AIRPORT"]=center
    return wp_coord
wp_coord = dict_coordinate()

wp_coord
"""
calcolo la distanza per ogni coppia
"""
def distanza_coppie(traj = trajectory,dict_wp = wp_coord):
    """
    INPUT:
        -lista di liste delle trajettorie
        -dizionario con le coordinate di ogni singolo waypoint_per_fl

    OUTPUT:
        -dizionario dove per ogni coppia (utile) di traiettorie ritorna la
            distanza

    """
    res = {}
    for i in range(len(traj)):
        traiettoria = traj[i]
        if len(traiettoria)==1:
            continue
        else:
            for j in range(len(traiettoria)-1):
                p1 = traiettoria[j]
                p2 = traiettoria[j+1]
                stringa = p1+"-"+p2
                c1 = wp_coord[p1]
                c2 = wp_coord[p2]
                dist=geodesic(c1,c2).kilometers
                if(stringa not in res):
                    res[stringa]=dist
    return res

dictionario_distanza_coppie = distanza_coppie()












def minimo_coppia(wp1,wp2,df=df_tot):
    """
    auxiliary function che calcola, dati due waypoint, il minimo tempo per
    passare dal primo al secondo
    """
    min = 100000000000
    for i in range(df.shape[0]-1):
        temp_i = df.iloc[i]
        temp_2i= df.iloc[i+1]
        if(temp_i["sid"]==wp1 and temp_2i["sid"]==wp2 and temp_i["aereo"]==temp_2i["aereo"]):
            if(temp_2i["time_sec"]-temp_i["time_sec"]<=min):
                min = temp_2i["time_sec"]-temp_i["time_sec"]
            if(temp_2i["time_sec"]-temp_i["time_sec"]<0):
                print(i)
    return min

lista_coppie = list(dictionario_distanza_coppie.keys())
lista_coppie

def tempi_minimi_coppie( lista_coppie = lista_coppie, df = df_tot):
    """
    INPUT :
        -lista_coppie = lista con tutte le coppie sotto forma di stringa
        -df = dataframe con i dati relativi agli aerei di un unica giornata

    OUTPUT:
        -dictionary dove per ogni coppia viene restituito il tempo minimo
    """
    res = {}
    for i in range(len(lista_coppie)):
        print(i)
        print(lista_coppie[i])
        print("*****************************")
        temp = lista_coppie[i]
        temp = temp.replace("-"," ")
        temp = temp.split(" ")
        c = minimo_coppia(temp[0],temp[1])
        res[lista_coppie[i]]=c
    return res



tempi_coppie = tempi_minimi_coppie()
tempi_coppie



def minimo_percorsi(tempi_coppie = tempi_coppie,df = df_tot,traj = trajectory):
    """
    INPUT:
        - tempi_coppie = dictionary con i minimi tempi per ogni coppia

    OUTPUT:
        -dictionary dove per ogni percorso c'è il tempo minimo calcolato sui minimo_coppia
        di ogni coppia che forma il percorso
    """
    res = {}

    for i in range(len(traj)):
        print(i)
        traiettoria = traj[i]
        print(traiettoria)

        s = ""
        tempo = 0
        #formo la stringa che andrà a descrivere la traiettoria
        for j in range(len(traiettoria)):
            if j<len(traiettoria)-1:
                s = s + traiettoria[j] + "-"
            else:
                s = s + traiettoria[j]
        # ora calcolo il tempo
        for j in range(len(traiettoria)-1):
            wp1 = traiettoria[j]
            wp2 = traiettoria[j+1]
            ss = wp1 + "-" + wp2
            tempo += tempi_coppie[ss]
        res[s]= tempo
        print(len(res))
        print("**********")

    return res

min_tempi_percorsi = minimo_percorsi()


"""
'RIMET-ODIPI-TUNIV-KERAX-GED-MTR-AIRPORT'
costruisco il dataframe dove c'è aereo-traiettoria-tempo_percorso-tempo_minimo-delay
"""

#ora ho la mia lista aerei
df_tot
def lista_aerei(df = df_tot):

    aerei = []
    i = 0
    while(i<df.shape[0]):
        aerei.append(df.iloc[i]["aereo"])
        j = i+1
        while(j<df.shape[0]-1 and df.iloc[i]["aereo"]==df.iloc[j]["aereo"]):
            j = j+1
        i = j+1
    return aerei

lista_aerei = lista_aerei()
df_tot

lista = ["aereo","traiettoria","partenza in sec","arrivo in sec","tempo percorso","tempo minimo","delay"]



prova = prova.append(pd.Series([a1,s,fine-inizio,min,(fine-inizio)-min], index=prova.columns),ignore_index=True)

def dataframe_traiettorie_minime(lista = lista ,df = df_tot, aircrafts = lista_aerei):
    min_tempi_percorsi = minimo_percorsi()
    res = pd.DataFrame(columns = lista)
    i = 0
    cont = 0
    while(i<df.shape[0]-1):
        s = ""
        a_temp = lista_aerei[cont]
        j = i
        inizio = df_tot.iloc[i]["time_sec"]
        while(j < df.shape[0]-1 and df_tot.iloc[j]["aereo"]==a_temp):
            s = s + df_tot.iloc[j]["sid"]+"-"
            j = j+1
        i = j
        fine = df_tot.iloc[i-1]["time_sec"]

        s = s[:-1]
        mini = 0
        if s in min_tempi_percorsi:
            mini = min_tempi_percorsi[s]
        else:
            mini = fine -inizio


        res = res.append(pd.Series([a_temp,s,inizio,fine,fine-inizio,mini,(fine-inizio)-mini], index=res.columns),ignore_index=True)

        cont = cont + 1
        print(i)
    return res


df_minimal = dataframe_traiettorie_minime()
df_minimal
