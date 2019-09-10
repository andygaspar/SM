import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun

df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")
#rinominazione colonna coordinate
df_wp.rename(columns={'astext(k.coords)':'coor'},inplace=True)


"""
DISTANZE

creazione del dataset con le distanze dall'aereoporto
"""
#costruzione del vettore distanza dall'areoporto per ogni waypoint


wp_dist=fun.df_coor_to_dist(df_wp)
df_wp["distance"]=wp_dist
#limitazione agli waypoint più vicini di 200km dall'aeroporto
entry_condition=df_wp['distance']<200
df_entry=df_wp[entry_condition]

"""
*****************************************************************
"""





"""
NUMERO DI WP PER VOLO
vettore
"""

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
np.sum(waypoint_per_fl==0)
len(waypoint_per_fl)

"""
***********************************************************
"""





"""
PER BUBBLEPLOT
DF DATA E ORA SEPARATE SENZA TRAIETTORIA, GEOPOINT
"""
#aggiunta colonna "data volo" e rimpiazzo colonna touch down con "time"
date=[]
landing=[]
df_wp_dist=df_entry.copy
for i in range(df_entry.shape[0]):
    kk=df_entry.iloc[i]["time_over"]
    kk=kk.split(" ")
    date.append(kk[0])
    landing.append(kk[1])


#tolte colonne inutili e aggiunte nuove
df_to_plot=df_entry.copy()
df_to_plot["date"]=date
df_to_plot["time"]=landing
df_to_plot=df_to_plot.drop(columns=["trajectory_id","geopoint_id","time_over"])
df_to_plot.shape
export_csv = df_to_plot.to_csv (r'../data/df_to_plot.csv', index = None, header=True)

"""
**************************************************
"""





"""

DF DATA E ORA SEPARATE SENZA TRAIETTORIA, GEOPOINT MA CON COORDINATE E COOR
"""
#aggiunta colonna "data volo" e rimpiazzo colonna touch down con "time"
date=[]
landing=[]
for i in range(df_entry.shape[0]):
    kk=df_entry.iloc[i]["time_over"]
    kk=kk.split(" ")
    date.append(kk[0])
    landing.append(kk[1])


#tolte colonne inutili e aggiunte nuove
df_entry["date"]=date
df_entry["time"]=landing
df_entry=df_entry.drop(columns=["trajectory_id","geopoint_id","time_over"])
df_entry.shape
#export_csv = df_toplot.to_csv (r'../data/df_entry.csv', index = None, header=True)

"""
**************************************************
"""










"""
aggiunta funzioni sul contteggio degli waypoint

è una lista con 5 dizionari ogniuno riferito ad
un wp, ordinati per numero di passaggi
"""



wp_dict_1={}
wp_dict_2={}
wp_dict_3={}stat_waypoint[4].key[0]
wp_dict_4={}
wp_dict_5={}
stat_waypoint=[wp_dict_1,wp_dict_2,wp_dict_3,wp_dict_4,wp_dict_5]


names=["wp1","wp2","wp3","wp4","wp5"]
for j in range(5):
    for i in range(df_traj.shape[0]):
        way_p=df_traj.iloc[i][names[j]]
        if way_p in stat_waypoint[j]:
            stat_waypoint[j][way_p]+=1
        else:
            stat_waypoint[j][way_p]=1

    #riordino dizionario
    stat_waypoint[j]=sorted(stat_waypoint[j].items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
    stat_waypoint[j]=dict(stat_waypoint[j])
stat_waypoint[0]
'REDNI' in stat_waypoint[0]













"""
******************** calcolo wp più frequenti
"""
df_wp_dist=pd.read_csv("../data/df_entry.csv")
entry_condition=df_wp_dist['distance']<200
df_wp_dist=df_wp_dist[entry_condition]
wp_dict={}
for i in range(df_wp_dist.shape[0]):
    way_p=df_wp_dist.iloc[i]["sid"]
    if way_p in wp_dict:
        wp_dict[way_p]+=1df_wp_dist=pd.read_csv("../data/df_entry.csv")
entry_condition=df_wp_dist['distance']<200
df_wp_dist=df_wp_dist[entry_condition]
    else:
        wp_dict[way_p]=1

#riordino dizionario
wp_dict=sorted(wp_dict.items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
wp_dict=dict(wp_dict)
wp_dict['UNOKO']
wp_dict
