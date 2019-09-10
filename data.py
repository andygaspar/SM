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
DF CON SOLO VOLI DI UNA DETERMINATA GIORNATA
"""


########################################### primo dataframe
cond_day1=df_entry["date"]=="2017-09-13"  #data in considerazione
df_entry_day1=df_entry[cond_day1]
df_entry_day1.shape

#creazione dataframe con ultimi waypoint
df_traj=pd.DataFrame(columns=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5'])

names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']

#creazione dataframe con ultimi waypoint
df_traj=pd.DataFrame(columns=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5'])


df_entry_day1
export_df = df_entry_day1.to_csv(r'../data/file.csv',index = None, header=True)

names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']
i=0
while i < df_entry_day1.shape[0]-1:
    row=[df_entry_day1.iloc[i]["ifps_id"],'None','None','None','None','None','None','None','None','None','None']
    j=1
    cont = 0 #contare quante volte si entra
    while (df_entry_day1.iloc[i]["ifps_id"]==df_entry_day1.iloc[i+1]["ifps_id"] and j<=4):
        j+=1
        cont = cont + 1
    if cont ==0:
        print("A SHIT")
        i = i+ 1
        continue
    for k in range(j):
        row[1+k]=df_entry_day1.iloc[i+j-k-1]["sid"]
        row[1+k+5]=df_entry_day1.iloc[i+j-k-1]["time"]
    df_traj=df_traj.append(dict(zip(names,row)),ignore_index = True)
    print("**********************************************")
    for m in range(len(row)):
        print(row[m])
    print("**********************************************")
    i+=j
    while (i<=df_entry_day1.shape[0]-2 and df_entry_day1.iloc[i]["ifps_id"]==df_entry_day1.iloc[i+1]["ifps_id"]):
        i+=1
    print("questa è la j:",j)
    #if(j>1):
    i+=1
    print(i)
df_traj
#ORA   : prendo il dataset relativo agli arrivi e lo pulisco nel modo seguente:
#   -considero gli arrivi solo a Francoforte cancellando le altre righe
#   -cancello la colonna relativa all'origine (inutile per noi)
#   -mettdf_wp_dist=pd.read_csv("../data/df_entry.csv")
entry_condition=df_wp_dist['distance']<200
df_wp_dist=df_wp_dist[entry_condition]o a posto le colo# Change the row indexes nne relative al timing (divido data e ora) e considero solo la nostra dataset

#dopo di chè dovrò creare la colonna arrivi

df_ar

#condizione di arrivo a Francoforte-->nuovo dataset con Francoforte
Frankfurt_cond = df_ar["D"]=="EDDF"
df_ar_frank = df_ar[Frankfurt_cond]
df_ar_frank

#metto a posto arr_time
arr_date = []
arr_land = []
for i in range(df_ar_frank.shape[0]):
    temp = df_ar_frank.iloc[i]["arr_time"]
    temp=temp.split(" ")
    arr_date.append(temp[0])
    arr_land.append(temp[1])


df_ar_frank["date"]=arr_date
df_ar_frank["time"]=arr_land

df_ar_frank= df_ar_frank.drop(columns=["O","arr_time"])

df_ar_frank

#considero solo i voli in data 2017-09-13
date_condition = df_ar_frank["date"]=="2017-09-13"
df_ar_frank_day1 = df_ar_frank[date_condition]


df_ar_frank_day1

#creiamo file csv di questi arrivi
arr_frankfurt_13_09_17 = df_ar_frank_day1.to_csv(r'../data/arr_frankfurt_13_09_17.csv',index = None, header=True)


arrivi = [] # non so se serve però intanto lo metto
voli = []
#ora la parte più difficile
for i in range(df_traj.shape[0]):
    flight = df_traj.iloc[i]["flight"]
    cont = 0
    for j in range(df_ar_frank_day1.shape[0]):
        aereo = df_ar_frank_day1.iloc[j]["ifps_id"]
        if(aereo==flight):
            cont = 1
            temp = df_ar_frank_day1.iloc[j]["time"]
            arrivi.append(temp)
    if(cont==0):
        arrivi.append("None")

    print(cont)


#aggiungo la colonna
len(arrivi)e={"a":1}
"a"in e


df_traj["arrival"] = arrivi


df_traj


"""
*****************************************************************
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
