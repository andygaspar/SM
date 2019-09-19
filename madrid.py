import pandas as pd
import numpy as np
from scipy.stats import chisquare
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import arrival_analysis as aa
import data as data
import csv
import copy
import simple_simulation as ss
import plot as p





#caricamento preliminari
d=pd.read_csv("../data/completo.csv")
d_ar=pd.read_csv("../data/arrivi_completo.csv")



#scelta aeroporto e filtro distanze
airport="LEMD"
capacita=75

lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste(airport)
lista_date.sort()
d_wp_coor=fun.dict_wp_coor(airport)
df=data.airport(d,airport)
df_ar=data.airport(d_ar,airport)
df=data.dist_filter(df,200)


#analisi frequenze
for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)
aa.freq_analysis(airport,lista_date)


#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date



#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=6
end_time=11



#scelta waypoint
wp=["ROLIS","UNOKO","KERAX","PSA"]



#creazione del df_finale per wp e tuttte le date nella lista (molto lento!!!!!!!)
df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
df_all_days


#calcolo frequenza media nella fascia oraria in tutte le date scelte
freq=aa.frequenza_media(start_time,end_time,airport,lista_date)
freq


#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)


#run del modello e calcolo della distribuzione
iterazioni=1000
sigma=10
sim,sim_matrix=ss.simulation_PRSA(iterazioni,capacita, start_time, end_time, freq, sigma)
sim_d=ss.sim_distribution(sim_matrix)


#calcolo delle code dai dati e della distribuzione relativa
#due metodi, truncated e rounded. questo perché
#delay/capacità=queue è decimale e va reso intero
data_queue_truncated=data.make_data_queue(df_busy,capacita)
data_queue_rounded=data.make_data_queue(df_busy,capacita,"rounded")
data_t=ss.data_distribution(data_queue_truncated)
data_r=ss.data_distribution(data_queue_rounded)



#plotting
plt.plot(sim_d,label="simulation_PRSA")
plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title("Distribution sigma=10")
plt.legend()
plt.show()
