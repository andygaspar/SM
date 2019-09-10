import numpy as np
from geopy.distance import geodesic


def coord(coordinate):
    coordinate=coordinate.replace("POINT","")
    coordinate=coordinate.replace("(","")
    coordinate=coordinate.replace(")","")
    split_coordinate=coordinate.split(" ")
    return [float(split_coordinate[0]),float(split_coordinate[1])]




def df_coor_to_dist(df):
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






"""  !!!!!!!!!! DA SISTEMARE
*********************************************************************
calcolo tempi arrivo
"""
df_traj
def time_to_sec(arr):
    arr=arr.replace(":"," ")
    arr=arr.split(" ")
    arr=int(arr[0])*3600  +  int(arr[1])*60   +  int(arr[2])come dataframe
    return arr

def percorrenza(entry,arr):
    return time_to_sec(arr)-time_to_sec(entry)


#lista percorrenza voli da SIRPO
def perc_per_waypoint(waypoint):
    perc=[]
    for i in range(df_traj.shape[0]):
        if df_traj.iloc[i]["wp1"]==waypoint:
            perc.append(percorrenza(df_traj.iloc[i]["t1"],df_traj.iloc[i]["arrival"]))
    return perc
a=perc_per_waypoint('SIRPO')
a=np.array(a)
np.mean(a)
