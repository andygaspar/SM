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

d=pd.read_csv("../data/completo.csv")
d_ar=pd.read_csv("../data/arrivi_completo.csv")

lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
lista_date.sort()
d_wp_coor=fun.dict_wp_coor()

"aeroporto destinazione"
airport="EDDF"
df=data.airport(d,airport)
df_ar=data.airport(d_ar,airport)
df=data.dist_filter(df,300)


help(data)

#analisi frequenze
for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)


#tolto il primo giorno perché inutile
lista_date=lista_date[1:-1]
lista_date


#creazione df_finale
other=["KERAX","PSA"]
wp=["ROLIS","UNOKO"]
date=lista_date[0]
dff=data.df_per_data(df,date)
dff_ar=data.df_per_data(df_ar,date)
dff_ar=df_ar.sort_values(by="time_sec")
df_delay,min_dict=data.df_finale_delay(dff,dff_ar,date,wp)

start_time=6
end_time=10.5

df_all_days=df_delay.copy()
denom=0
f=0
for i in range(1,len(lista_date)):
    date=lista_date[i]
    dff=data.df_per_data(df,date)
    dff_ar=data.df_per_data(df_ar,date)
    dff_ar=df_ar.sort_values(by="time_sec")
    df_delay,min_dict=data.df_finale_delay(dff,dff_ar,date,wp)
    df_all_days=df_all_days.append(df_delay)
    freq,df_arr_busy=aa.freq_busy(start_time,end_time,date,airport)
    f+=freq*df_arr_busy.shape[0]
    denom+=df_arr_busy.shape[0]
    print(i,freq,df_arr_busy.shape[0])

freq=f/denom

df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)



sim,sim_matrix=ss.simulation_PRSA(1000, start_time, end_time, freq, 5)
sim_d=ss.sim_distribution(sim_matrix)

data_queue=delay/freq

data_q=ss.data_distribution(np.round(data_queue))
data_d=ss.data_distribution(data_queue.astype(int))

plt.plot(sim_d)
plt.plot(data_d)
plt.plot(data_q)
