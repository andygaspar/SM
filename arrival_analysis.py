import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data



def sec_to_time(x):
    sec=x%60
    x-=sec
    min=int(x/60)%60
    x-=min
    h=int(x/3600)
    return str(h)+":"+str(min)+":"+str(sec)

df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")


#separazione colonne data e tempo e aggiunta colonna tempo in secondi
data.data_time(df_ar,"arr_time")
data.add_time_in_sec(df_ar)
data.data_time(df_wp)
df_ar

#solo una giornata
cond=df_ar["date"]==df_ar.iloc[0]["date"]
df_new=df_ar[cond]
df_new


#vettore tempo in sec degli arrivi, ordinato
arrival=df_new["time_sec"].values
arrival=np.array(sorted(arrival))

arrival_time=[]
for i in arrival:
    arrival_time.append(sec_to_time(i))



#distribuzione frequenza nelle ore della giornata

p=plt.hist(arrival,bins=48)
p.set_xticklabels(range(24))
plt.show()



#selezione in base al plot della fascia oraria le 5-21
len(arrival)
cond=arrival>5*3600
busy_arrival=arrival[cond]
len(busy_arrival)
cond=busy_arrival<21*3600
busy_arrival=busy_arrival[cond]
len(busy_arrival)
sec_to_time(busy_arrival[-1])



#calcolo frequenza
freq=(21-5)*3600/len(busy_arrival)
freq
