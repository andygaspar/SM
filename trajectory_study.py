import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data
from numpy import linalg as LA
from scipy.spatial import distance


df_ar=pd.read_csv("../data/arrivi_completo.csv")
df_wp=pd.read_csv("../data/completo.csv")


data.rinomina(df_wp,"astext(k.coords)","coor")
data.add_dist(df_wp)
df_filtered=data.dist_filter(df_wp,200)

df_filtered
freq = fun.frequency(df_filtered,"sid")

cond = df_filtered["date"]=="2017-09-13"
df_filtered=df_filtered[cond]
df_filtered
pp = df_filtered.to_csv("../c.csv")

coordinate = []
#mettiamo a posto le coordinate
for i in range(df_filtered.shape[0]):
    coordinate.append(fun.coord(df_filtered.iloc[i]["coor"]))

df_filtered= df_filtered.drop(columns=["coor"])
df_filtered["coor"]=coordinate



"""
Ora procedo con la costruzione del dataset: in questo dataset ci saranno le traiettorie_13_09
relative ai voli avvenuti il giorno 13 settembre nell'aereoporto di Frankfurt.
Per semplicità (da migliorare) consideriamo solo i flight con più di 5 waypoint e
consideriamo solo i primi 5 waypoint [ai fini del tempo è importante il primo]
"""



names=['flight','wp1','wp2','wp3','wp4','wp5','t1','t2','t3','t4','t5']
df_filtered
df_traj = data.creation_data_waypoint(df_filtered,names,name_of_col ="aereo")
df_traj







"""
Al dataset creato aggiungo gli arrivi, contenuti nel dataset df_ar
"""
data.rinomina(df_ar,"flight","aereo")
data.rinomina(df_traj,"flight","aereo")
df_ar
cond = df_ar["date"]=="2017-09-13"
df_ar=df_ar[cond]
df_traj = data.arrival_matching(df_traj,df_ar)
df_traj

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

traiettorie_day1 = df_traj.to_csv(r'../traiettorie_day1.csv',index = None, header=True)



none_cond = df_traj["arrival"]!="None"
df_traj = df_traj[none_cond]
#######fare  vettore di traiettorie
df_traj

"""
ora creo un dict, chiamato tr_dict, che ha come chiavi tutte le pox traiettorie_13_09
e come valori il numero di volte che queste traiettorie appaiono

"""
trajectory = []
df_traj
barra = "-"
for i in range(df_traj.shape[0]):
    percorso = df_traj.iloc[i]["wp1"]+barra+df_traj.iloc[i]["wp2"]+barra+df_traj.iloc[i]["wp3"]+barra+df_traj.iloc[i]["wp4"]+barra+df_traj.iloc[i]["wp5"]
    trajectory.append(percorso)

trajectory

"trovo tutti gli entry points"


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
t

percorsi = list(tr_dict.keys()) #lista di tutte le pox traiettorie
num_percorsi = list(tr_dict.values()) #lista del numero di volte in cui le traiettorie si presentano
len(percorsi)



"""
Ora creo un dict,chiamato wp_coord, che ha come chiavi tutti i pox waypoints
e come valori le loro coordinate
"""
wp_coord ={}
for i in range(df_filtered.shape[0]):
    sid = df_filtered.iloc[i]["sid"]
    if sid not in wp_coord:
        wp_coord[sid] = df_filtered.iloc[i]["coor"]
    else:
        continue

wayp = list(wp_coord.keys()) #lista di tutti i waypoint
wayp
wp_c = list(wp_coord.values())
wp_coord_df = pd.DataFrame(wp_coord,columns=["waypoints","coord"])

wp_coord_df


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

























lista_wp = list(wp_coord.keys())
lista_coordinate = list(wp_coord.values())









list_freq = list(freq.keys())

list_freq_2 = []
for i in range(10):
    list_freq_2.append(list_freq[i])


wp_freq=list(freq.keys())

wp_freq_l = wp_freq[:5]


wp_freq_l

plt.figure(figsize=(20,15))
plt.rc('font', size=15)
plt.rc('axes', titlesize=15)
for i in range(coord_traj.shape[0]):
    tr = coord_traj.iloc[i]
    if(i<2):
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and tr["wp4"]!="None" and tr["wp5"]!="None"):
            plt.plot(coordinate_y[i,:],coordinate_x[i,:],linewidth=num_percorsi[i]/10,label = "trajectory "+str(i))

        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]!="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_y[i,:-1],coordinate_x[i,:-1],linewidth=num_percorsi[i]/10)
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]=="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_y[i,:-2],coordinate_x[i,:-2],linewidth=num_percorsi[i]/10)

        else:
            continue
    if(i>=2):
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and tr["wp4"]!="None" and tr["wp5"]!="None"):
            plt.plot(coordinate_y[i,:],coordinate_x[i,:],linewidth=num_percorsi[i]/10)

        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]!="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_y[i,:-1],coordinate_x[i,:-1],linewidth=num_percorsi[i]/10)
        if(tr["wp1"]!="None" and tr["wp2"]!="None" and tr["wp3"]!="None" and
            tr["wp4"]=="None" and tr["wp5"]=="None"):
                plt.plot(coordinate_y[i,:-2],coordinate_x[i,:-2],linewidth=num_percorsi[i]/10)
        else:
            continue
coor_dict=fun.dict_wp_coor(airport)
N=len(wp_list)
x=np.zeros(N)
y=np.zeros(N)
z=np.zeros(N)
i=0
fr_dict=fun.dict_wp_freq(airport)
for key in wp_list:
    c=fun.coord(coor_dict[key])
    x[i]=c[0]
    y[i]=c[1]
    z[i]=fr_dict[key]
    i=i+1
#plt.figure(figsize=(20,15))
    #plt.scatter(y,x ,s=z*0.3, alpha=al)
lon=8.560964
lat=50.037753
AIR="FR AIRPORT"
plt.scatter( lon,lat,color="red",s=150)
plt.annotate(AIR,xy=(lon,lat),xytext=(lon-0.3, lat-0.1),size=textsize+1)
for wp in wp_list:
    c=fun.coord(coor_dict[wp])
    plt.scatter(c[1],c[0],color="green")
    plt.annotate(wp,xy=(c[1],c[0]),xytext=(c[1]-0.08, c[0]-0.08),size=textsize)

plt.scatter(8.560964,50.037753,color="red",linewidth=2)
plt.annotate("Airport",xy=(8.560964,50.037753), xytext=(8.560964-0.20,50.037753 -0.20),arrowprops=dict(facecolor='black', shrink=0.05))
plt.title("Airport map")
plt.xlabel("x coordinate")
plt.ylabel("y coordinate")
for i in range(len(wayp)):

    wp = wp_freq[i]
    for j in  range(len(wp_coord)):
        if wp==wayp[j] and ((wp =="PSA" or wp=="KERAX" or wp=="ROLIS" or wp=="UNOKO")) :

            plt.scatter(coord_of_wp[j][1],coord_of_wp[j][0])
            plt.annotate(wp+" "+str(i),xy=(coord_of_wp[j][1],coord_of_wp[j][0]), xytext=(coord_of_wp[j][1]-0.15,coord_of_wp[j][0] -0.15),arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend()
plt.savefig("../../results/traj_1_bis_bis.png")
plt.show()
