import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data
import csv
import copy


df=pd.read_csv("../data/completo.csv")
df=data.dist_filter(df,200)
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()
df=data.df_per_data(df,lista_date[0])
df

main=["KERAX","PSA","ROLIS","UNOKO"]



trajectory=traiettorie_complete(df)



def traiettorie_complete(df):
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





def shift_coor(d_wp_coor):len(traj_list)
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
CREAZIONE WP_COORD
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
                if(stringa not in w):
                    res[stringa]=dist
    return res

dictionario_distanza_coppie = distanza_coppie()






pr = trajectory[0]
df

cont = 0
for i in range(len(pr)-1):
    p1 = df.iloc[i]
    p2=df.iloc[i+1]
    t1 = p1["time_sec"]
    t2 = p2["time_sec"]
    cont += t2-t1

cont = df.iloc[len(pr)-1]["time_sec"] - df.iloc[0]["time_sec"]

cont
#1029

def tempo_di_percorrenza_percorsi(df = df,traj = trajectory):
    res = []
    i = 0

    lunghezza = 0
    for cont in range(len(traj)):
        temp = traj[cont]
        lunghezza = len(temp) - 1
        if len(temp)==1:
            res.append(0)
            i = i+1+lunghezza
        
        else:
            tp = df.iloc[lunghezza + i]["time_sec"] - df.iloc[i]["time_sec"]
            res.append(tp)
        i = i+1+lunghezza

    return res


q = tempo_di_percorrenza_percorsi()
len(q)
len(trajectory)
def merge_percorsi_tempi(traj = trajectory,df = df):
    tempi = tempo_di_percorrenza_percorsi(df,traj)
    res = {}
    for i in range(len(traj)):
        #trasformo i percorsi in stringhe
        traiettoria = traj[i]
        s = ""
        for j in range(len(traiettoria)):
            if(j<len(traiettoria)-1):
                s = s+traiettoria[j]+"-"
            else:
                s = s+traiettoria[j]
        print(s)
        if(s not in res):
            res[s]=tempi[i]
    return res



pp = merge_percorsi_tempi()
