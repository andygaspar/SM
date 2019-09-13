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
