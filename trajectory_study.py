import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data


df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")
df_toplot = pd.read_csv("../data/df_to_plot.csv")
df_wp
data.rinomina(df_wp,"astext(k.coords)","coor")
data.add_dist(df_wp)
df_filtered=data.dist_filter(df_wp,200)

df_filtered
freq = fun.frequency(df_filtered,"sid")


df_wp



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
df_entry_day1

i = 0
names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']
sl = list(s.values())
sl[3]
df_traj = da.creation_data_waypoint(df_entry_day1,names)
df_traj

df_entry_day1





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
percorsi


"""
TROVO TERZA TRIAETTORIA
"""
df_traj
tr_interessante = percorsi[2]
tr_interessante = tr_interessante.replace("-"," ")
tr_interessante = tr_interessante.split(" ")
tr_interessante
temp = list(df_traj.iloc[0])
temp[1]==tr_interessante[0]
aereo = " "


aereo

aircraft_condition = df_wp["ifps_id"]==aereo
ddf = df_wp[aircraft_condition]
ddf.shape[0]
condd = ddf["distance"]<200

ddf = ddf[condd]

ddf
tr_interessante = ddf["sid"].values
tr_interessante = list(tr_interessante)
tr_interessante


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
df_wp

tr_dict

wp_coord




s =aircraft_repetition(df_entry_day1,"ifps_id")
s

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
freq
for i in range(10):
    temp = lista_traiet[i]
    temp = temp.replace("-"," ")
    temp = temp.split(" ")
    wp_imp.append(temp[0])
print("*****")
wp_imp
lista = list(freq.keys())
lista



list_freq
liste_freq_value = list(freq.values())
coord_imp = []
list_freq = lista[0:20]

len(list_freq)
for i in tr_interessante:
    coord_imp.append(wp_coord[i])

coord_imp

int_dict = dict(zip(tr_interessante,coord_imp))
int_dict
entrance_dict = dict(zip(list_freq,coord_imp))
entrance_dict
entrance_dict["CHA"][0]

"""
***************************************************************
"""
"""
VEDO LE TRAIETTORIE IMPORTANTI COMPLETE
"""
"""
**************************************************************
"""

tr_dict
tr = list(tr_dict.keys())
tr = tr[0:20]
tr
aircrafts = []


for j in range(len(tr)):
    temp_tr = tr[j]
    temp_tr=temp_tr.replace("-"," ")
    temp_tr = temp_tr.split(" ")
    for i in range(df_traj.shape[0]):
        temp = df_traj.iloc[i]
        if(temp_tr[0]==temp["wp1"] and temp_tr[1]==temp["wp2"] and temp_tr[2]==temp["wp3"] and
           temp_tr[3]==temp["wp4"] and temp_tr[4]==temp["wp5"]):
           aircrafts.append(temp["flight"])
           break

df_wp
aircrafts
d_cond = df_wp["distance"]<200
df_wp = df_wp[d_cond]
df_cond = df_wp["ifps_id"]==aircrafts[0]
df = df_wp[df_cond]
df
tr_sing = df["sid"].values
tr_sing
def traiettorie_complete(lista_aircrafts):
    traiettorie = []
    for i in range(len(aircrafts)):
        tr = lista_aircrafts[i]
        df_cond = df_wp["ifps_id"]==tr
        df = df_wp[df_cond]
        tr_sing = list(df["sid"].values)
        traiettorie.append(tr_sing)
    return traiettorie


traiettorie  = traiettorie_complete(aircrafts)
traiettorie[0]
wp_coord
lista_coordinate = list(wp_coord.values())
lista_wp = list(wp_coord.keys())
lista_coordinate

coord_traiettorie = []




def coordinate_list(traiettoria,lista_wp,lista_coordinate):
    N = len(traiettoria)
    coordinate_x = np.zeros(N)
    coordinate_y = np.zeros(N)
    for i in range(N):
        st = traiettoria[i]
        for j in range(len(lista_wp)):
            if(st==lista_wp[j]):
                coordinate_x[i]=lista_coordinate[j][0]
                coordinate_y[i]=lista_coordinate[j][1]
    return coordinate_x,coordinate_y



p,q = coordinate_list(traiettorie[0],lista_wp,lista_coordinate)
plt.plot(p,q)

"""
provo a plottare le traiettorie
"""

p,q =
plt.figure(figsize=(20,15))
for i in range(len(traiettorie)):
    tr_i = traiettorie[i]
    print(tr_i)
    x_cord,y_cord = coordinate_list(tr_i,lista_wp,lista_coordinate)
    plt.plot(x_cord,y_cord,)
plt.scatter(50.037753, 8.560964,color="red")
for i in int_dict:
    plt.scatter(int_dict[i][0], int_dict[i][1],linewidth = 6,label = i)
    plt.annotate(i,xy=(int_dict[i][0],int_dict[i][1]), xytext=(int_dict[i][0]-0.25,int_dict[i][1] -0.25),arrowprops=dict(facecolor='red', shrink=0.05))








freq
list_freq = list(freq.keys())
list_freq
list_freq_2 = []
for i in range(10):
    list_freq_2.append(list_freq[i])
list_freq_2
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
for i in entrance_dict:
    plt.scatter(entrance_dict[i][0], entrance_dict[i][1],linewidth = 6,label = i)
    plt.annotate(i,xy=(entrance_dict[i][0],entrance_dict[i][1]), xytext=(entrance_dict[i][0]-0.15,entrance_dict[i][1] -0.15),arrowprops=dict(facecolor='black', shrink=0.05))
for i in int_dict:
    plt.scatter(int_dict[i][0], int_dict[i][1],linewidth = 6,label = i)
    plt.annotate(i,xy=(int_dict[i][0],int_dict[i][1]), xytext=(int_dict[i][0]-0.25,int_dict[i][1] -0.25),arrowprops=dict(facecolor='red', shrink=0.05))


plt.legend()
plt.savefig("plot/traj_1_bis.png")

plt.show()


help(fun.frequency)
