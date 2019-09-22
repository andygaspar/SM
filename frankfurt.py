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
airport="EDDF"
capacita=80

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
start_time=4
end_time=19




#scelta waypoint
wp=["ROLIS","UNOKO","KERAX","PSA"]



#creazione del df_finale per wp e tuttte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
#data.save_df(df_all_days,"francoforte.csv")
df_all_days=pd.read_csv("francoforte.csv")





#ricaviamo il valre della capacità e della frequenza (che nel nostro modello sono uguali)
def trovo_capacity(start_time, end_time, df = df_ar):
    """
    funzione che calcola
    """
    dfarr=data.df_per_data(df_ar,lista_date)
    dfarr=data.df_fascia_oraria(dfarr,start_time,end_time)
    capacita=3600/(dfarr.shape[0]/(len(lista_date)*(end_time-start_time)))
    return capacita



capacita = trovo_capacity(start_time,end_time)



#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)



#run del modello e calcolo della distribuzione
capacita=freq
sigma=10

iterazioni=200
len_periodo=14
sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo ,capacita, freq,sigma)
sim_norm=ss.sim_distribution(sim_matrix)
sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo ,capacita, freq,sigma,"uni")
sim_uni=ss.sim_distribution(sim_matrix)





data_queue_truncated=data.make_data_queue(df_busy,capacita)
data_queue_rounded=data.make_data_queue(df_busy,capacita,"rounded")
data_t=ss.data_distribution(data_queue_truncated)
data_r=ss.data_distribution(data_queue_rounded)



#plotting
plt.plot(sim_norm,label="simulation_NORM")
plt.plot(sim_uni,label="simulation_UNI")


plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" FRANKFURT sigma="+str(sigma)+" noise="+str(noise))
plt.legend()
plt.show()





distribuzioni=[sim_norm,sim_uni,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual














l_sigma=np.arange(10,20.5,0.5)
PAR,min_sig,mat_sig=fun.parameter(14,l_sigma,freq,capacita,df_busy,200)

min_sig
np.min(PAR)
PAR

l_sigma=np.arange(5,31,2.5)
l_noise=np.arange(0,0.21,0.025)

l_sigma[4]
l_noise[3]



fig=plt.figure()
ax=fig.gca(projection="3d")

x,y=np.meshgrid(l_noise,l_sigma)
ax.plot_surface(x,y,PAR)
plt.show()
x.shape
PAR.shape
