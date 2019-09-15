import numpy as np
from geopy.distance import geodesic
import csv
import pandas as pd
import data as data


"  frequenze **********************"

def frequency(df,label):
    """
    dato un datafreme e una label
    ritorna un dict ordinato con le frequenze
    """
    fr_dic={}
    for i in range(df.shape[0]):
        key=df.iloc[i][label]
        if key in fr_dic:
            fr_dic[key]+=1
        else:
            fr_dic[key]=1

    #riordino dizionario
    fr_dic=sorted(fr_dic.items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
    return dict(fr_dic)




"funzioni coordinate e waypoint ***************"

def coord(coordinate):
    """
    data una stringa di coordinate
    restituisce una lista con le coordinate in float
    """
    coordinate=coordinate.replace("POINT","")
    coordinate=coordinate.replace("(","")
    coordinate=coordinate.replace(")","")
    split_coordinate=coordinate.split(" ")
    return [float(split_coordinate[0]),float(split_coordinate[1])]


def df_coor_to_dist(df):
    """
    dato un df con la colonna coor
    ritorna un np.array con le distanze dall'aeroporto
    """
    AIRPORT=(50.03793, 8.56215)
    wp_dist=np.zeros(df.shape[0])
    for i in range(df.shape[0]):
        coordinate=df["coor"][i]
        coordinate=coordinate.replace("POINT","")
        coordinate=coordinate.replace("(","")
        coordinate=coordinate.replace(")","")
        split_coordinate=coordinate.split(" ")
        split_coordinate=[float(split_coordinate[0]),float(split_coordinate[1])]
        ENTRY=tuple(split_coordinate)
        dist=geodesic(ENTRY,AIRPORT).kilometers
        wp_dist[i]=dist
    return wp_dist


def wp_neighbours(wp,dist_max):
    """
    dato un wp e un raggio
    crea una lista degli wp in quel raggio
    """
    wp_dict=dict_wp_coor()
    neighbours=[]

    coordinate=wp_dict[wp]
    coordinate=coordinate.replace("POINT","")
    coordinate=coordinate.replace("(","")
    coordinate=coordinate.replace(")","")
    split_coordinate=coordinate.split(" ")
    split_coordinate=[float(split_coordinate[0]),float(split_coordinate[1])]
    WP=tuple(split_coordinate)

    for key in wp_dict:
        if key!=wp:
            coordinate=wp_dict[key]
            coordinate=coordinate.replace("POINT","")
            coordinate=coordinate.replace("(","")
            coordinate=coordinate.replace(")","")
            split_coordinate=coordinate.split(" ")
            split_coordinate=[float(split_coordinate[0]),float(split_coordinate[1])]
            NEIGH=tuple(split_coordinate)
            dist=geodesic(WP,NEIGH).kilometers
            if dist<=dist_max:
                neighbours.append(key)
    return neighbours


def dict_wp_coor():
    """
    crea dict wp:coordinate
    """
    wp_coordinate=[]
    with open('../data/wp_coor.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            wp_coordinate.append(row)

    wp=[]
    with open('../data/lista_wp.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            wp.append(row)
    wp_coor=dict(zip(wp[0],wp_coordinate[0]))
    return wp_coor


def shift_coor(d_wp_coor):
    """
    dato il dict_wp_coor (wp:coordinate)
    shifta le coordinate vicino all'origine
    ritorna 2 liste: scaled_long,scaled_lat
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








"  funzioni tempo ******************************"


def time_to_sec(arr):
    """
    dato il tempo hh:mm:ss
    restituisce il valore numerico in secondi:
    int(arr[0])*3600  +  int(arr[1])*60   +  int(arr[2])
    """
    arr=arr.replace(":"," ")
    arr=arr.split(" ")
    arr=int(arr[0])*3600  +  int(arr[1])*60   +  int(arr[2])
    return arr


def sec_to_time(x):
    """
    fun inversa di time_to_sec
    """
    sec=x%60
    x-=sec
    min=int(x/60)%60
    x-=min
    h=int(x/3600)
    return str(h)+":"+str(min)+":"+str(sec)


def tempo_volo(entry,arr):
    """
    dato entry_time e arrival_time numerici
    ritorna il tempo di percorrenza

    """
    if type(entry)==str:
        return time_to_sec(arr)-time_to_sec(entry)
    else:
        return arr-entry


def min_time_dict(df,lista):
    """
    dato un dataframe ed una lista di wp
    ritorna un dict con {wp: min_time}
    """
    min_t={}
    for wp in lista:
        cond=df["sid"]==wp
        df_aux=df[cond]
        m=min(df_aux["fly time"])
        min_t[wp]=min(df_aux["fly time"])

    return min_t




"  funzioni traiettorie ********************************+"


def traiettorie_complete(df):
    """
    dato un df
    crea lista con tutte le traiettorie
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


"  funzioni statistiche *****************************"
def reject_outliers(data, m=2):
    """
    dato un array e un fattore moltiplicativo
    ritorna un array senza gli outliers
    """
    return data[abs(data - np.mean(data)) < m * np.std(data)]
