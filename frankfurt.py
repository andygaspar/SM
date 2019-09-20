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
import random as rm






#caricamento preliminari
d=pd.read_csv("../data/completo.csv")
d_ar=pd.read_csv("../data/arrivi_completo.csv")



#scelta aeroporto e filtro distanze
airport="EDDF"


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
end_time=10




#scelta waypoint
wp=["ROLIS","UNOKO","KERAX","PSA"]



#creazione del df_finale per wp e tuttte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
#data.save_df(df_all_days,"francoforte.csv")
df_all_days=pd.read_csv("francoforte.csv")


#calcolo frequenza media nella fascia oraria in tutte le date scelte
freq=aa.frequenza_media(start_time,end_time,airport,lista_date)
freq


#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)


#definisco la variabile load traffic ro
ro,max=aa.find_ro(freq,start_time,end_time,lista_date,airport)
ro



#run del modello e calcolo della distribuzione
capacita=max/ro
capacita
sigma=9.0
noise=0.0
iterazioni=1000
sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise)
sim_norm=ss.sim_distribution(sim_matrix)
sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"uni")
sim_uni=ss.sim_distribution(sim_matrix)
sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"exp")
sim_exp=ss.sim_distribution(sim_matrix)



#calcolo delle code dai dati e della distribuzione relativa
#due metodi, truncated e rounded. questo perché
#delay/capacità=queue è decimale e va reso intero
data_queue_truncated=data.make_data_queue(df_busy,capacita)
data_queue_rounded=data.make_data_queue(df_busy,capacita,"rounded")
data_t=ss.data_distribution(data_queue_truncated)
data_r=ss.data_distribution(data_queue_rounded)



#plotting
plt.plot(sim_norm,label="simulation_NORM")
plt.plot(sim_uni,label="simulation_UNI")
plt.plot(sim_exp,label="simulation_EXP")
#plt.plot(sim_tri,label="simulation_TRI")
plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" FRANKFURT sigma="+str(sigma)+" noise="+str(noise))
plt.legend()
plt.show()





distribuzioni=[sim_norm,sim_uni,sim_exp,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
D
qual=fun.quality(D)
qual















PAR,min_sig,dist_min=fun.parameter(start_time,end_time,freq,freq,df_busy,1000,noise=False)
min_sig

plt.plot(np.arange(5,21,0.5),PAR)
plt.grid()

dist_min
