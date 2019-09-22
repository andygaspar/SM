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

"""
TROVIAMO WAYPOINTS PIU' VICINI AD ARRIVO E PLOTTIAMOLI
"""
 #vettore delle traiettorie

wp1 = []
for i in range(len(trajectory)):
    temp = trajectory[i]
    temp = temp.replace("-"," ")
    temp = temp.split(" ")
    if temp[0] not in wp1:
        wp1.append(temp[0])
    else:
        continue

wp1 #ordinati
wp_coord
coord_of_wp = list(wp_coord.values())
type(coord_of_wp[0][1])
wayp
#provo a plottarli
plt.figure(figsize=(20,15))
for i in range(len(wp1)):
    wp = wp1[i]
    print(wp)
    for j in  range(len(wp_coord)):
        if wp==wayp[j]:
            print("ciao")
            plt.scatter(coord_of_wp[j][0],coord_of_wp[j][1],label = wp)
plt.show()























lista_wp = list(wp_coord.keys())
lista_coordinate = list(wp_coord.values())









list_freq = list(freq.keys())

list_freq_2 = []
for i in range(10):
    list_freq_2.append(list_freq[i])


wp_freq=list(freq.keys())

plt.figure(figsize=(20,15))
for i in range(coord_traj.shape[0]):
    tr = coord_traj.iloc[i]
    if(i<5):
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
    if(i>=5):
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
plt.scatter(8.560964,50.037753,color="red")
for i in range(len(wayp)):

    wp = wp_freq[i]
    for j in  range(len(wp_coord)):
        if wp==wayp[j] and ((wp =="PSA" or wp=="KERAX" or wp=="ROLIS" or wp=="UNOKO") or wp in wp_freq_l) :

            plt.scatter(coord_of_wp[j][1],coord_of_wp[j][0])
            plt.annotate(wp+" "+str(i),xy=(coord_of_wp[j][1],coord_of_wp[j][0]), xytext=(coord_of_wp[j][1]-0.15,coord_of_wp[j][0] -0.15),arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend()
plt.savefig("plot/traj_1_bis_bis.png")
plt.show()
w



for i in range(len(trajectory)):
    print(trajectory[i])
    trajectory[i] = trajectory[i].replace("-"," ")
    trajectory[i] = trajectory[i].split(" ")
trajectory


#sperimentiamo

def distance_trajectory(tr1,tr2):
    """
    tr1 e tr2 sono traiettorie già divise in una lista
    df è il dict con le coordinate di ogni way_point
    """
    n1 = 0
    n2 = 0
    for i in range(len(tr1)):
        if(tr1[i]!="None"):
            n1+=1
    for i in range(len(tr2)):
        if(tr2[i]!="None"):
            n2+=1
    dist = []
    if(n1==n2):
        for j in range(n1):
            dist.append(distance.euclidean(wp_coord[tr1[j]],wp_coord[tr2[j]]))
    if (n1!=n2):
        minimo = min(n1,n2)

        for j in range(minimo):
            dist.append(distance.euclidean(wp_coord[tr1[j]], wp_coord[tr2[j]]))
    dist = np.array(dist)
    return dist.mean()



p_arr = percorsi.copy()
for i in range(len(p_arr)):
    p_arr[i] = p_arr[i].replace("-"," ")
    p_arr[i] = p_arr[i].split(" ")

p_arr

# vediamo quante trajettorie sono "simili alla traiettoria 0"













"""
stessa cosa con il secondo
"""


def controlla_traiettoria(trajectories,df = df_traj):
    voli = []
    for j in range(df.shape[0]):
        aircraft = df.iloc[j]["flight"]
        cond = df["flight"]==aircraft
        x = df[cond]
        x = x.iloc[0]
        x = x[1:6]
        x = list(x)
        for i in range(len(trajectories)):
            if(x==trajectories[i]):
                if(aircraft not in voli):
                    voli.append(aircraft)
                break
            else:
                continue
    return voli



qwerty=controlla_traiettoria(similar_to_one)

d



"scrivo una funzione che restituisca due liste:"
"la prima da la traiettoria simile ad una determinata traiettoria"
"la seconda le coordinate"



trajectory

def trova_percorsi_simili(tr_princ,d,trajectories = trajectory):
    similar = []
    for i in range(len(trajectories)):
        dist = distance_trajectory(tr_princ,trajectories[i])
        if (dist< d and trajectories[i] not in similar and trajectories[i]!=tr_princ):
            similar.append(trajectories[i])

    similar_cord = []
    for i in range(len(similar)):
        temp = similar[i]
        coord = []
        for j in range(len(temp)):
            if (temp[j]!="None"):
                coord.append(wp_coord[temp[j]])
            else:
                coord.append(0)
        similar_cord.append(coord)
    return similar,similar_cord

coordinate_x
tr_dict


def coordinate_list(traiettoria,lista_wp=lista_wp,lista_coordinate=lista_coordinate):
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



def plotting_percorsi_simili(tr_princ,sim,sim_cord):
    coordinate_x,coordinate_y = coordinate_list(tr_princ)
    plt.figure(figsize=(20,15))
    for i in range(len(sim_cord)):
        x = []
        y = []
        for j in range(5):
            if(sim_cord[i][j]!=0):
                x.append(sim_cord[i][j][0])
                y.append(sim_cord[i][j][1])
        plt.plot(x,y,linewidth=1)
    plt.scatter(50.037753, 8.560964,color="red")



a,b = trova_percorsi_simili(p_arr[0],1)
c,d =trova_percorsi_simili(p_arr[1],1)
plotting_percorsi_simili(p_arr[0],a,b)
plotting_percorsi_simili(p_arr[1],c,d)
plt.plot(coordinate_x[0],coordinate_y[0],linewidth=10,label = "trajectory_1")
plt.legend()
plt.show()



"""
CLUSTERING
"""
df_traj
cont = 0
p_arr
len(tr_dict)
list_sim = []
list_sim_cord = []
i=0
percorsi_trovati = []
while(i<10):
    print("len",len(trajectory))
    sim_i,sim_i_cord = trova_percorsi_simili(p_arr[i],1.0)
    print(sim_i)
    for j in range(len(sim_i)):
        if sim_i[j] in trajectory:
            trajectory.remove(sim_i[j])
        else:
            print("boh")
    print("len traj",trajectory)
    list_sim.append(sim_i)
    list_sim_cord.append(sim_i_cord)
    print(i)
    i=i+1
len(list_sim)

for m in range(3):
    plotting_percorsi_simili(p_arr[m],list_sim[m],list_sim_cord[m])
    plt.plot(coordinate_x[m],coordinate_y[m],linewidth=10,label = "trajectory_"+str(m))
    plt.scatter(50.037753, 8.560964,color="red")
    for i in range(10):
        wp = wp_freq[i]
        for j in  range(len(wp_coord)):
            if wp==wayp[j]:
                plt.scatter(coord_of_wp[j][0],coord_of_wp[j][1])
                plt.annotate(wp+" "+str(i),xy=(coord_of_wp[j][0],coord_of_wp[j][1]), xytext=(coord_of_wp[j][0]-0.15,coord_of_wp[j][1] -0.15),arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend()
plt.show()
len(trajectory)

list_sim[0]
aircraft = list(df_traj["flight"])
aircraft
df_traj
#quali aircraft passano per il primo gruppo ?
air_1 = []
air_2 = []
for i in range(len(aircraft)):
    line = df_traj.iloc[i]
    aircr = df_traj.iloc[i]["flight"]
    for j in range(len(list_sim[0])):
        if(line["wp1"]==list_sim[0][j][0] and line["wp2"]==list_sim[0][j][1] and
            line["wp3"]==list_sim[0][j][2] and line["wp4"]==list_sim[0][j][3] and
            line["wp5"]==list_sim[0][j][4]):
            air_1.append(aircr)
            break
        else:
            continue

len(air_1)
for i in range(len(aircraft)):
    line = df_traj.iloc[i]
    aircr = df_traj.iloc[i]["flight"]
    for j in range(len(list_sim[1])):
        if(line["wp1"]==list_sim[1][j][0] and line["wp2"]==list_sim[1][j][1] and
            line["wp3"]==list_sim[1][j][2] and line["wp4"]==list_sim[1][j][3] and
            line["wp5"]==list_sim[1][j][4]):
            air_2.append(aircr)
            break
        else:
            continue



len(air_2)

for i in range(len(aircraft)):
    line = df_traj.iloc[i]
    aircr = df_traj.iloc[i]["flight"]
    for j in range(len(list_sim[1])):
        if(line["wp1"]==list_sim[1][j][0] and line["wp2"]==list_sim[1][j][1] and
            line["wp3"]==list_sim[1][j][2] and line["wp4"]==list_sim[1][j][3] and
            line["wp5"]==list_sim[1][j][4]):
            air_2.append(aircr)
            break
        else:
            continue

wp_coord
wp_dict
def raggruppa_aerei(list_sim,index,air_list="aircr",df=df_traj):
     air = []
     for i in range(len(aircraft)):
         line = df.iloc[i]
         aircr = line["flight"]
         for j in range(len(list_sim[0])):
             if(line["wp1"]==list_sim[1][j][0] and line["wp2"]==list_sim[1][j][1] and
                 line["wp3"]==list_sim[1][j][2] and line["wp4"]==list_sim[1][j][3] and
                 line["wp5"]==list_sim[1][j][4]):
                 air.append(aircr)
                 break
             else:
                 continue
     return air


air_1 = raggruppa_aerei(list_sim,0)

len(air_1)



for i in range()
