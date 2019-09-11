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



def percorrenza(entry,arr):
    """
    UTILE ALLA FUN PERC_PER_WAYPOINT
    dato entry_time e arrival_time numerici
    ritorna il tempo di percorrenza

    """
    return time_to_sec(arr)-time_to_sec(entry)



def perc_per_waypoint(waypoint):
    """
    dati due waypoints calcola il tempo di percorrenza
    """
    perc=[]
    for i in range(df_traj.shape[0]):
        if df_traj.iloc[i]["wp1"]==waypoint:
            perc.append(percorrenza(df_traj.iloc[i]["t1"],df_traj.iloc[i]["arrival"]))
    return perc



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


def arrival_matching(df_wp,df_arrivi,col_flights = "flight"):
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
