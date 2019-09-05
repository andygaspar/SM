import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt

df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")
df_wp.rename(columns={'astext(k.coords)':'coor'},inplace=True)

"""
    #calcolo distanza da areoporto
    AIRPORT=(50.03793, 8.56215)
    dist=geodesic(ENTRY,AIRPORT).kilometers
    dist



    # rielaborazione stringhe
    df_wp.head(100)
    type(df_wp["coor"][2])
    test=df_wp["coor"][2]
    test
    test=test.replace("POINT","")
    test=test.replace("(","")
    test=test.replace(")","")
    test
    split_test=test.split(" ")
    split_test
    split_test=[float(split_test[0]),float(split_test[1])]
    split_test=tuple(split_test)
    split_test


    #primo test su primo volo
    flight_1=df_wp['ifps_id']=="AA66960337"

    flight_1=df_wp[flight_1]
    flight_1

    #ricerca per caratteristtica, crea oggetto true false che può essere letto da df
    ar_1=df_ar['ifps_id']=="AA66960337"
    #df da oggetto true false
    ar_fl_1=df_ar[ar_1]
    ar_fl_1


    df_wp.shape
    n=flight_1=df_wp['sid']=="ODIPI"

    prova=df_wp[n]
    prova.loc[,"trajectory_id"]
    type(prova)
    prova["astext(k.coords)"]




"""








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
        wp_dist[i]=dist[waypoint_per_fl==0]
    #df_wp_dist.rename(columns={'coor':'distance'},inplace=True)
    return wp_dist

wp_dist=df_coor_to_dist(df_wp)
df_wp["distance"]=wp_dist
#df_wp.to_csv()


entry_condition=df_wp['distance']<200
df_entry=df_wp[entry_condition]

#df_entry.to_csv(path_or_buf="../data")



#vettore numero di waypoint per volo
waypoint_per_fl=[]
j=0
for i in range(df_entry.shape[0]-1):
    if df_entry.iloc[i]["ifps_id"]==df_entry.iloc[i+1]["ifps_id"]:
        j+=1
    else:
        waypoint_per_fl.append(j)
        j=0
waypoint_per_fl=np.array(waypoint_per_fl)
np.min(waypoint_per_fl)
np.mean(waypoint_per_fl)
waypoint_per_fl=sorted(waypoint_per_fl)
plt.plot(waypoint_per_fl)
np.sum(waypoint_per_fl==10)




kk=df_entry.iloc[0]["time_over"]
kk=kk.split(" ")
kk=kk[0]
kk


#aggiiunta colonna data e rimpiazzo colonna touch down
date=[]
landing=[]
for i in range(df_entry.shape[0]):
    kk=df_entry.iloc[i]["time_over"]
    kk=kk.split(" ")
    date.append(kk[0])
    landing.append(kk[1])


# df_entry.drop(columns="date")
# df_entry.drop(columns="date")

#tolte colonne inutili
df_entry["date"]=date
df_entry["time"]=landing
df_entry=df_entry.drop(columns=["trajectory_id","geopoint_id","time_over","coor"])







########################################### primo dataframe
cond_day1=df_entry["date"]=="2017-09-13"
df_entry_day1=df_entry[cond_day1]
df_entry_day1.shape

#creazione dataframe con ultimi waypoint
df_traj=pd.DataFrame(columns=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5'])



names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']
i=0
while i < df_entry_day1.shape[0]-1:
    row=[df_entry_day1.iloc[i]["ifps_id"],'None','None','None','None','None','None','None','None','None','None']
    j=1
    while (df_entry_day1.iloc[i]["ifps_id"]==df_entry_day1.iloc[i+1]["ifps_id"] and j<=4):
        j+=1
    for k in range(j):
        row[1+k]=df_entry_day1.iloc[i+j-k-1]["sid"]
        row[1+k+5]=df_entry_day1.iloc[i+j-k-1]["time"]
    df_traj=df_traj.append(dict(zip(names,row)))
    i+=j
    while (i<=df_entry_day1.shape[0]-2 and df_entry_day1.iloc[i]["ifps_id"]==df_entry_day1.iloc[i+1]["ifps_id"]):
        i+=1
    print(i)
df_traj
