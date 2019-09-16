import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data
import csv
import copy


df=pd.read_csv("../data/completo.csv")
df_ar = pd.read_csv("../data/arrivi_1709.csv")
df=data.dist_filter(df,200)
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()
df=data.df_per_data(df,'2017-08-17')
df

main=["KERAX","PSA","ROLIS","UNOKO"]


#lavoro solo su una data



"""
"""


df_ar
df_ar =data.data_time(df_ar,"arr_time")
cond = df_ar["date"]=='2017-08-17'
df_ar =df_ar[cond]
df_ar






trajectory=traiettorie_complete(df)
trajectory[1]





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


df


def shift_coor(d_wp_coor):
    len(traj_list)
    """
    dato il dict_wp_coor
    shift coordinate vicino all'origine
    """
    long=[]
    lat=[]
    for i in d_wp_coor:
        c=fun.coord(d_wp_coor[i])
        long.append(c[0])
        lat.append(c[1])
    long=np.array(long)
    lat=np.array(lat)
    mlong=min(long)
    mlat=min(lat)
    scaled_long=long-mlong
    scaled_lat=lat-mlat
    return scaled_long,scaled_lat



scaled_long,scaled_lat=shift_coor(d_wp_coor)
plt.scatter(scaled_long,scaled_lat)





"""
CREAZIONE WP_COORD--> da funzionalizzare
"""
df.shape[0]
cc = df.iloc[0]["coor"]
cc=cc.replace("POINT","")
cc
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


len(trajectory)


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

dictionario_distanza_coppie["MTR-ORVIV"]
trajectory
len(trajectory)

dictionario_distanza_coppie





def trovo_ripetizioni(perc,tr = trajectory):
    """
    INPUT: perc: percorso d'interesse, introdotto come array dove ogni
                waypoint è un elemento distinto
          tr : dataframe con tutti i ipercorsi
    OUTPUT: array con indici relativi alle ripetizioni del percorso di input
    """
    res = []
    for i in range(len(tr)):
        if(perc == tr[i]):
            res.append(i)

    return res


ì

len(trajectory)

cont = 0
for i in range(len(trajectory)):
    tr = trajectory[i]
    for j in range(len(tr)-1):
        if(tr[j]=="MTR" and tr[j+1]=="ORVIV"):
            print(i)
            print(tr)
            cont+=1
            print("************************************************")

cont
df

def minimo_coppia(wp1,wp2,df=df):
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

dictionario_distanza_coppie = distanza_coppie()
lista_coppie = list(dictionario_distanza_coppie.keys())
lista_coppie
dictionario_distanza_coppie["MTR-ORVIV"]

def tempi_minimi_coppie( lista_coppie = lista_coppie, df = df):
    """
    INPUT :
        -lista_coppie = lista con tutte le coppie sotto forma di stringa
        -df = dataframe con i dati relativi agli aerei di un unica giornata

    OUTPUT:
        -dictionary dove per ogni coppia viene restituito il tempo minimo
    """
    res = {}
    for i in range(len(lista_coppie)):
        temp = lista_coppie[i]
        temp = temp.replace("-"," ")
        temp = temp.split(" ")
        c = minimo_coppia(temp[0],temp[1])
        res[lista_coppie[i]]=c
    return res

tempi_coppie = tempi_minimi_coppie()
tempi_coppie
tempi_coppie["MTR-ORVIV"]

trajectory


def minimo_percorsi(tempi_coppie = tempi_coppie,df = df,traj = trajectory):
    """
    INPUT:
        - tempi_coppie = dictionary con i minimi tempi per ogni coppia

    OUTPUT:
        -dictionary dove per ogni percorso c'è il tempo minimo calcolato sui minimo_coppia
        di ogni coppia che forma il percorso
    """
    res = {}
    for i in range(len(traj)):
        traiettoria = traj[i]
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
    return res

min_tempi_percorsi = minimo_percorsi()
len(min_tempi_percorsi)
