import numpy as np
from geopy.distance import geodesic
import csv
import pandas as pd
import data as data
import simple_simulation as ss


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





def dict_wp_freq(airport):
    """
    crea dict wp: frequenze
    """
    lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste(airport)

    return dict(zip(lista_wp,lista_freq_wp))


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
    F=(50.03793,8.56215)
    H=(51.469911,-0.454269)
    M=(40.494817,-3.567995)
    wp_dist=np.zeros(df.shape[0])
    for i in range(df.shape[0]):
        coordinate=df["coor"][i]
        coordinate=coordinate.replace("POINT","")
        coordinate=coordinate.replace("(","")
        coordinate=coordinate.replace(")","")
        split_coordinate=coordinate.split(" ")
        split_coordinate=[float(split_coordinate[0]),float(split_coordinate[1])]
        ENTRY=tuple(split_coordinate)
        if df.iloc[i]["D"]=="EDDF":
            dist=geodesic(ENTRY,F).kilometers
        if df.iloc[i]["D"]=="EGLL":
            dist=geodesic(ENTRY,H).kilometers
        if df.iloc[i]["D"]=="LEMD":
            dist=geodesic(ENTRY,M).kilometers
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


def dict_wp_coor(airport):
    """
    crea dict wp:coordinate
    """

    if airport=="EDDF":
        wpl='../data/lista_wp.csv'
        wpc='../data/wp_coor.csv'

    if airport=="EGLL":
        wpl='../data/lista_wp_H.csv'
        wpc='../data/lista_coor_M.csv'

    if airport=="LEMD":
        wpl='../data/lista_wp_M.csv'
        wpc='../data/lista_coor_M.csv'

    wp_coordinate=[]
    with open(wpc) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            wp_coordinate.append(row)

    wp=[]
    with open(wpl) as csv_file:
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


def tot_variation(p,q):
    return sum(abs(p-q))/2

def hellinger(p,q):
    return np.sqrt(sum((np.sqrt(p)-np.sqrt(q))**2))*1/np.sqrt(2)

def standardise_len(lista_distrib):
    max=0
    new_list=[lista_distrib[0]]
    for d in lista_distrib:
        if len(d)>max:
            max=len(d)
            new_list[0]=d

    for d in lista_distrib[1:]:
        if len(d)<max:
            d=np.append(d,np.zeros(max-len(d)))
            new_list.append(d)
        if len(d)==max:
            new_list.append(d)

    return new_list



def dist_mat(l_distrib):
    N=len(l_distrib)
    mat=np.zeros((N-1,4))
    for i in range(N-1):
        mat[i,0]=tot_variation(l_distrib[i],l_distrib[3])
        mat[i,1]=hellinger(l_distrib[i],l_distrib[3])
        mat[i,2]=tot_variation(l_distrib[i],l_distrib[4])
        mat[i,3]=hellinger(l_distrib[i],l_distrib[4])

    return mat

def quality(mat):
    return sum(sum(mat[0:-1]))


def parameter(start_time,end_time,freq,capacita,df_busy,iterazioni):
    l_sigma=np.arange(5,31,2.5)
    l_noise=np.arange(0,0.21,0.025)
    mat=np.zeros((len(l_sigma),len(l_noise)))

    i=0
    for sigma in l_sigma:
        j=0
        for noise in l_noise:
            sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise)
            sim_norm=ss.sim_distribution(sim_matrix)
            sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"uni")
            sim_uni=ss.sim_distribution(sim_matrix)
            sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"exp")
            sim_exp=ss.sim_distribution(sim_matrix)



            data_queue_truncated=data.make_data_queue(df_busy,capacita)
            data_queue_rounded=data.make_data_queue(df_busy,capacita,"rounded")
            data_t=ss.data_distribution(data_queue_truncated)
            data_r=ss.data_distribution(data_queue_rounded)


            distribuzioni=[sim_norm,sim_uni,sim_exp,data_t,data_r]
            distrib=standardise_len(distribuzioni)

            mat[i,j]=quality(dist_mat(distrib))
            j+=1
        i+=1
    return mat
