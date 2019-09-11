import numpy as np
from geopy.distance import geodesic


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



def time_to_sec(arr):
    """
    UTILE ALLA FUN PERCORRENZA
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



"Da finire ***********************"
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
        print(m)
        min_t[wp]=min(df_aux["fly time"])

    return min_t
