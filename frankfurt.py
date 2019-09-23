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


lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste(airport)
lista_date.sort()
d_wp_coor=fun.dict_wp_coor(airport)
df=data.airport(d,airport)
df_ar=data.airport(d_ar,airport)
df=data.dist_filter(df,200)
df_ar

#analisi frequenze
for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)
aa.freq_analysis(airport,lista_date)




#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)
lista_date



#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=[5,12.5]
end_time=[10,18.5]




#scelta waypoint
wp=["ROLIS","UNOKO","KERAX","PSA"]



#creazione del df_finale per wp e tuttte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
#data.save_df(df_all_days,"francoforte.csv")
df_all_days=pd.read_csv("francoforte.csv")





#ricaviamo il valre della capacità e della frequenza (che nel nostro modello sono uguali)




capacita = aa.find_capacity(start_time,end_time,df_ar,lista_date)

capacita

#df_finale filtrato con solo la fascia oraria di interesse

df_busy=data.df_busy(df_all_days,start_time[0],end_time[0])
df_busy,delay=data.sort_df(df_busy)

for i in range(1,len(start_time)):
    df_busy_i=data.df_busy(df_all_days,start_time[i],end_time[i])
    df_busy_i,delay=data.sort_df(df_busy_i)
    df_busy=df_busy.append(df_busy_i)

df_busy

#run del modello e calcolo della distribuzione
freq = capacita
sigma=5.5
freq
iterazioni=200
len_periodo=11
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
plt.title(" FRANKFURT sigma="+str(sigma))
plt.legend()
plt.show()
plt.savefig("results/Frankfurt.png")





distribuzioni=[sim_norm,sim_uni,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual

D



l_sigma=np.arange(4,12.5,0.5)
P=[]
ms=[]
mt=[]
for i in range(20):
    PAR,min_sig,mat_sig=fun.parameter(11,l_sigma,freq,capacita,df_busy,200)
    P.append(PAR)
    ms.append(min_sig)
    mt.append(mat_sig)


Pr=np.array(P)
M=np.zeros(Pr.shape[1])
for i in range(len(M)):
    M[i]=np.mean(Pr[:,i])




for i in range(len(Pr)):
    plt.plot(np.arange(4,12.5,0.5),Pr[i],linewidth=0.5)
plt.plot(np.arange(4,12.5,0.5),M,linewidth=8,label = "mean plot")
plt.xlabel(" possible value of sigma")
plt.ylabel("quality value")
plt.legend()
plt.savefig("results/frankfurt_sigmas.png")
