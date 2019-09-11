import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as da


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
df_entry_day1
"""
Ora procedo con la costruzione del dataset: in questo dataset ci saranno le traiettorie_13_09
relative ai voli avvenuti il giorno 13 settembre nell'aereoporto di Frankfurt.
Per semplicità (da migliorare) consideriamo solo i flight con più di 5 waypoint e
consideriamo solo i primi 5 waypoint [ai fini del tempo è importante il primo]
"""


i = 0
names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']
df_traj = da.creation_data_waypoint(df_entry_day1,names)
df_traj






"""
Al dataset creato aggiungo gli arrivi, contenuti nel dataset df_ar
"""
arr = pd.read_csv("../data/arr_frankfurt_13_09_17.csv")

arr
df_traj = da.arrival_matching(df_traj,arr)

#df_traj rappresenta i primi 5 waypoints e i vari tempi + tempo arrivo
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
len(percorsi)
num_percorsi
"""
Ora creo un dict,chiamato wp_coord, che ha come chiavi tutti i pox waypoints
e come valori le loro coordinate
"""
wp_coord ={}
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
    if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and tr["wp4"]!="None" and tr["wp5"]!="None"):
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

    if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
        tr["wp4"]!="None" and tr["wp5"]=="None"):
        coordinate_x[i,0]=tr["coord1"][0]
        coordinate_x[i,1]=tr["coord2"][0]
        coordinate_x[i,2]=tr["coord3"][0]
        coordinate_x[i,3]=tr["coord4"][0]

        coordinate_y[i,0]=tr["coord1"][1]
        coordinate_y[i,1]=tr["coord2"][1]
        coordinate_y[i,2]=tr["coord3"][1]
        coordinate_y[i,3]=tr["coord4"][1]

    if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
        tr["wp4"]=="None" and tr["wp5"]=="None"):
        coordinate_x[i,0]=tr["coord1"][0]
        coordinate_x[i,1]=tr["coord2"][0]
        coordinate_x[i,2]=tr["coord3"][0]


        coordinate_y[i,0]=tr["coord1"][1]
        coordinate_y[i,1]=tr["coord2"][1]
        coordinate_y[i,2]=tr["coord3"][1]

    else:
        continue

tr_dict
wp_coord


"""
************************************
"""
"""
PUNTI IMPORTANTI
"""

"""
**************************************
"""

lista_traiet = list(tr_dict.keys())
lista_traiet
wp_imp = []
for i in range(10):
    temp = lista_traiet[i]
    temp = temp.replace("-"," ")
    temp = temp.split(" ")
    wp_imp.append(temp[0])
print("*****")
wp_imp
coord_imp = []
for i in range(len(wp_imp)):
    coord_imp.append(wp_coord[wp_imp[i]])

entrance_dict = dict(zip(wp_imp,coord_imp))
entrance_dict
entrance_dict['KERAX'][0]


coordinate_x[1,:]
coordinate_x[1,:-2]
plt.figure(figsize=(20,15))
for i in range(coord_traj.shape[0]):
    tr = coord_traj.iloc[i]
    if(i<3):
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and tr["wp4"]!="None" and tr["wp5"]!="None"):
            plt.plot(coordinate_x[i,:],coordinate_y[i,:],linewidth=num_percorsi[i]/10,label = "trajectory "+str(i))

        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]!="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_x[i,:-1],coordinate_y[i,:-1],linewidth=num_percorsi[i]/10)
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]=="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_x[i,:-2],coordinate_y[i,:-2],linewidth=num_percorsi[i]/10)
        else:
            continue
    if(i>=3):
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and tr["wp4"]!="None" and tr["wp5"]!="None"):
            plt.plot(coordinate_x[i,:],coordinate_y[i,:],linewidth=num_percorsi[i]/10)

        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]!="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_x[i,:-1],coordinate_y[i,:-1],linewidth=num_percorsi[i]/10)
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]=="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_x[i,:-2],coordinate_y[i,:-2],linewidth=num_percorsi[i]/10)
        else:
            continue
plt.scatter(50.037753, 8.560964,color="red")
for i in wp_imp:
    plt.scatter(entrance_dict[i][0], entrance_dict[i][1],linewidth = 6,label = i)

plt.savefig("plot/traj_1.png")
plt.legend()
plt.show()


help(fun.frequency)
