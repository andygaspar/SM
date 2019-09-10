import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun


df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")
df_toplot = pd.read_csv("../data/df_to_plot.csv")




df_toplot

#considero solo un giorno e solo la condizione di frankfurt!
cond_day1=df_toplot["date"]=="2017-09-13"  #data in considerazione
df_entry_day1=df_toplot[cond_day1]
df_entry_day1.shape
df_entry_day1
f_cont = df_entry_day1["D"]="EDDF"
df_entry_day1=df_entry_day1[cond_day1]
df_entry_day1.shape
df_entry_day1

coordinate = []
#mettiamo a posto le coordinate
for i in range(df_entry_day1.shape[0]):
    coordinate.append(fun.coord(df_entry_day1.iloc[i]["coor"]))

df_entry_day1= df_entry_day1.drop(columns=["coor"])
df_entry_day1["coor"]=coordinate
df_entry_day1.shape[0]

p= df_entry_day1.to_csv (r'../data/ppt.csv', index = None, header=True)

"""
Ora procedo con la costruzione del dataset: in questo dataset ci saranno le traiettorie_13_09
relative ai voli avvenuti il giorno 13 settembre nell'aereoporto di Frankfurt.
Per semplicità (da migliorare) consideriamo solo i flight con più di 5 waypoint e
consideriamo solo i primi 5 waypoint [ai fini del tempo è importante il primo]
"""
df_traj=pd.DataFrame(columns=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5'])
i = 0
names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']
while(i<df_entry_day1.shape[0]-1):
    aereo = df_entry_day1.iloc[i]["ifps_id"]
    row=[aereo,'None','None','None','None','None','None','None','None','None','None']
    print("lavoriamo su questo aereo: ",aereo)
    cont = 1  # numero di stack relative a questo aereoporto
    j = i #da cove iniziamo a contare
    while(cont<=4 and aereo == df_entry_day1.iloc[j+1]["ifps_id"]):
        j = j+1 # andiamo avanti di un indice
        cont =cont+1 #contiamo gli stack
    print(cont)
    if(cont==5):
        for k in range(cont):
            #print("k: ",k)
            #print("i+j-k-1",i+j-k-1)
            row[1+k] = df_entry_day1.iloc[i+cont-k-1]["sid"]
            row[1+k+5]=df_entry_day1.iloc[i+cont-k-1]["time"]
        df_traj=df_traj.append(dict(zip(names,row)),ignore_index = True)
        i=j
        while (i<=df_entry_day1.shape[0]-2 and df_entry_day1.iloc[i]["ifps_id"]==df_entry_day1.iloc[i+1]["ifps_id"]):
            i+=1
        i+=1
    else:
        i=j
        #while (i<=df_entry_day1.shape[0]-2 and df_entry_day1.iloc[i]["ifps_id"]==df_entry_day1.iloc[i+1]["ifps_id"]):
        #    i+=1
        i+=1
    print(i)


"""
Al dataset creato aggiungo gli arrivi, contenuti nel dataset df_ar
"""
df_traj
Frankfurt_cond = df_ar["D"]=="EDDF"
df_ar_frank = df_ar[Frankfurt_cond]
df_ar_frank


arr_date = []
arr_land = []
for i in range(df_ar_frank.shape[0]):
    temp = df_ar_frank.iloc[i]["arr_time"]
    temp=temp.split(" ")
    arr_date.append(temp[0])
    arr_land.append(temp[1])


df_ar_frank["date"]=arr_date
df_ar_frank["time"]=arr_land

df_ar_frank

df_ar_frank= df_ar_frank.drop(columns=["O","arr_time"])

df_ar_frank.rename(columns={'ifps_id':'flight'},inplace=True)

date_condition = df_ar_frank["date"]=="2017-09-13"
df_ar_frank_day1 = df_ar_frank[date_condition]


df_ar_frank_day1


arr_frankfurt_13_09_17 = df_ar_frank_day1.to_csv(r'../data/arr_frankfurt_13_09_17.csv',index = None, header=True)



arrivi = [] # non so se serve però intanto lo metto
arrivi
voli = []
#ora la parte più difficile
for i in range(df_traj.shape[0]):
    flight = df_traj.iloc[i]["flight"]
    cont = 0
    for j in range(df_ar_frank_day1.shape[0]):
        aereo = df_ar_frank_day1.iloc[j]["flight"]
        if(aereo==flight):
            cont = 1
            temp = df_ar_frank_day1.iloc[j]["time"]
            arrivi.append(temp)
    if(cont==0):
        arrivi.append("None")

    print(cont)

df_traj["arrival"] = arrivi


df_traj

arrivi = df_traj.to_csv(r'../data/arrivi_13_09.csv',index = None, header=True)

#controllo
"""
for i in range(df_traj.shape[0]):
    if(df_traj.iloc[i]["arrival"]!="None"):
        b = fun.time_to_sec(df_traj.iloc[i]["arrival"])
        a = fun.time_to_sec(df_traj.iloc[i]["t1"])
        if(b-a<0):
            print("problema alla riga ",i)
    else:
        continue
"""


#df_traj rappresenta i primi 5 waypoints e i vari tempi
#ora aggiungo le tempistiche
tempistiche = []
for i in  range(df_traj.shape[0]):
    if (df_traj.iloc[i]["arrival"]=="None"):
        tempistiche.append("None")
    else:
        b = fun.time_to_sec(df_traj.iloc[i]["arrival"])
        a = fun.time_to_sec(df_traj.iloc[i]["t1"])
        tempistiche.append(b-a)
        if(b-a<=0):
            print("fuck off")

"aggiungo anche i tempi di arrivo"
df_traj["tempi di arrivo"] = tempistiche

######################################

df_traj

traiettorie_13_09 = df_traj.to_csv(r'../data/traiettorie_13_09.csv',index = None, header=True)

none_cond = df_traj["arrival"]!="None"
df_traj = df_traj[none_cond]
#######fare  vettore di traiettorie
df_traj

"""
ora creo un dict, chiamato tr_dict, che ha come chiavi tutte le pox traiettorie_13_09
e come valori il numero di volte che queste traiettorie appaiono

"""
trajectory = []

barra = "-"
for i in range(df_traj.shape[0]):
    percorso = df_traj.iloc[i]["wp1"]+barra+df_traj.iloc[i]["wp2"]+barra+df_traj.iloc[i]["wp3"]+barra+df_traj.iloc[i]["wp4"]+barra+df_traj.iloc[i]["wp5"]
    trajectory.append(percorso)


trajectory
len(trajectory)


#contare quante traiettorie ci sono e quante volte compaiono
tr_dict = {}
for i in range(len(trajectory)):
    tr = trajectory[i]
    if (tr in tr_dict):
        continue
    else:
        ripetizioni = trajectory.count(tr)
        tr_dict[tr] = ripetizioni

tr_dict= sorted(tr_dict.items(),key =lambda kv:(kv[1], kv[0]),reverse=True)
tr_dict = dict(tr_dict)
tr_dict

percorsi = list(tr_dict.keys()) #lista di tutte le pox traiettorie
num_percorsi = list(tr_dict.values()) #lista del numero di volte in cui le traiettorie si presentano
num_percorsi
len(percorsi)

"""
Ora creo un dict,chiamato wp_coord, che ha come chiavi tutti i pox waypoints
e come valori le loro coordinate
"""

wp_coord ={}

#riprendo il dataframe  df_entry_day1
df_entry_day1["sid"]

for i in range(df_entry_day1.shape[0]):
    sid = df_entry_day1.iloc[i]["sid"]
    if sid not in wp_coord:
        wp_coord[sid] = df_entry_day1.iloc[i]["coor"]
    else:
        continue

wayp = list(wp_coord.keys()) #lista di tutti i waypoint
wayp
wp_coord
cord_list = list(wp_coord.values()) #lista di tutte le coordinate
cord_list
#ora ogni percorso salvato in tr_dict avrà la sua coordinata
#ci sono 119 percorsi

"""
Ora creo un Dataframe, chiamato coord_traj, il quale contiene per ogni
traiettoria le coordinate di ogni singolo waypoint attraversato dalla TRAIETTORIA
in più contiene il numero di volte che questa traiettori viene percorsa

"""
name = ["wp1","wp2","wp3","wp4","wp5","coord1","coord2","coord3","coord4","coord5","times"]

coord_traj=pd.DataFrame(columns=["wp1","wp2","wp3","wp4","wp5","coord1","coord2","coord3","coord4","coord5","times"])


coord_traj

for i in range(len(percorsi)):
    perc =percorsi[i]
    perc=perc.replace("-"," ")
    perc=perc.split(" ") #ora è un vettore di 5 elementi
    row = []
    for m in range(5):
        row.append(perc[m])
    for j in range(5):
        temp = perc[j]
        for k in range(len(wayp)):
            if (temp==wayp[k]):
                row.append(cord_list[k])
            else:
                continue
    # ora ho row completamente--> aggiungo riga al dataframe
    row.append(num_percorsi[i])
    coord_traj=coord_traj.append(dict(zip(name,row)),ignore_index = True)


coord_traj
#proviamo a disegnare il primo percorso


"""
plotto le traiettorie
"""


coordinate_x = np.zeros((coord_traj.shape[0],5))
coordinate_y = np.zeros((coord_traj.shape[0],5))
#provo a plottare tutti i perorsi
for i in range(coord_traj.shape[0]):
    tr = coord_traj.iloc[i]
    coordinate_x[i,0]=tr["coord1"][0]
    coordinate_x[i,1]=tr["coord2"][0]
    coordinate_x[i,2]=tr["coord3"][0]
    coordinate_x[i,3]=tr["coord4"][0]
    coordinate_x[i,4]=tr["coord5"][0]
    coordinate_y[i,0]=tr["coord1"][1]
    coordinate_y[i,1]=tr["coord2"][1]
    coordinate_y[i,2]=tr["coord3"][1]
    coordinate_y[i,3]=tr["coord4"][1]
    coordinate_y[i,4]=tr["coord5"][1]


for i in range(coord_traj.shape[0]):
    plt.plot(coordinate_x[i,:],coordinate_y[i,:],linewidth=num_percorsi[i]/10,label = "trajectory"+str(i))
plt.scatter(50.037753, 8.560964,color="red")
#plt.legend()
plt.show()
