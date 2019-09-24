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



lista_date.pop(0)
lista_date.pop(-1)
#analisi frequenze
for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)
aa.freq_analysis(airport,lista_date)


"""
df_ar=pd.read_csv("../data/arrivi_completo.csv")
arr_day=data.airport(df_ar,airport)
to_plot=np.zeros(24)
for i in range(24):
    cond=arr_day["time_sec"]>=i*3600
    busy_arrival=arr_day[cond]
    cond=busy_arrival["time_sec"]<(i+1)*3600
    busy_arrival=busy_arrival[cond]
    to_plot[i]=busy_arrival.shape[0]
plt.plot(range(24),to_plot/len(lista_date))
plt.xlabel("Hours")
plt.xticks(np.arange(0, 24, 1))
plt.grid(b=True,axis='both')
plt.title(" mean of arrival rate")
plt.savefig("../../results/mean_arrival_madrid")
plt.show()
"""


#tolto il primo giorno perché inutile come si vede dai grafici

len(lista_date)



#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=[7,16]
end_time=[13,20]

capacita = aa.find_capacity(start_time,end_time,df_ar,lista_date)

capacita
d_freq=fun.dict_wp_freq("LEMD")
d_freq
d_freq["ORBIS"]


#scelta waypoint
wp=["TERSA","PRADO","BAN","ORBIS"]



#creazione del df_finale per wp e tuttte le date nella lista (molto lento!!!!!!!)
df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
df_all_days


#calcolo frequenza media nella fascia oraria in tutte le date scelte
capacita=aa.frequenza_media(7,12.5,airport,lista_date)

capacita_1=aa.frequenza_media(16,20.30,airport,lista_date)
capacita=(capacita+capacita_1)/2



#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,7,12.5)
df_busy=df_busy[df_busy["delay"]<1500]
df_busy,delay=data.sort_df(df_busy)


df_busy1=data.df_busy(df_all_days,16,20.5)
df_busy1=df_busy1[df_busy1["delay"]<1500]
df_busy1,delay=data.sort_df(df_busy1)

df_busy=df_busy.append(df_busy1)



#run del modello e calcolo della distribuzione
capacita
freq=capacita





sigma=4
iterazioni=400
len_periodo=13.5
sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo ,capacita,sigma)
sim_norm=ss.sim_distribution(sim_matrix)
sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo,capacita,sigma,"uni")
sim_uni=ss.sim_distribution(sim_matrix)
#sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo,capacita, freq,sigma,"exp")
#sim_exp=ss.sim_distribution(sim_matrix)
#sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"tri")
#sim_tri=ss.sim_distribution(sim_matrix)



#calcolo delle code dai dati e della distribuzione relativa
#due metodi, truncated e rounded. questo perché
#delay/capacità=queue è decimale e va reso intero
data_queue_truncated=data.make_data_queue(df_busy,capacita)
data_queue_rounded=data.make_data_queue(df_busy,capacita,"rounded")
data_t=ss.data_distribution(data_queue_truncated)
data_r=ss.data_distribution(data_queue_rounded)

plt.plot(sim)
plt.bar(range(len(sim_uni)),sim_uni)
#plotting
plt.figure(figsize=(10,5))
plt.rc('font', size=10)
plt.rc('axes', titlesize=10)

plt.plot(sim_norm,label="simulation_NORM")
plt.plot(sim_uni,label="simulation_UNI")
plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" MADRID with Omega="+str(sigma))
plt.legend()
plt.savefig("../../results/madrid_plots.png")
plt.show()
plt.savefig("../../results/madrid_plots.png")

len(sim_uni) #12
len(sim_norm) #13
len(data_r) #15
len(data_t) #15

Z = np.arange(13)
X = np.arange(12)
fig = plt.figure()
plt.figure(figsize=(60,30))

plt.rc('font', size=40)
plt.rc('axes', titlesize=40)


plt.subplot(2, 2, 1)
plt.bar(Z+0.00,sim_norm, color = 'b', width = 0.30,label = "normal distribution")
plt.bar(Z+0.30,data_r[:13], color = 'r', width = 0.30,label = "data rounded")

plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()

plt.subplot(2, 2, 2)
plt.bar(Z+0.00,sim_norm, color = 'b', width = 0.30,label = "normal distribution")
plt.bar(Z+0.30,data_t[:13], color = 'r', width = 0.30,label = "data truncated")
plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()

plt.subplot(2, 2, 3)
plt.bar(X+0.00,sim_uni, color = 'b', width = 0.30,label = "uniform distribution")
plt.bar(X+0.30,data_r[:12], color = 'r', width = 0.30,label = "data rounded")
plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()


plt.subplot(2, 2, 4)
plt.bar(X+0.00,sim_uni, color = 'b', width = 0.30,label = "uniform distribution")
plt.bar(X+0.30,data_t[:12], color = 'r', width = 0.30,label = "data truncated")
plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()

plt.savefig("../../results/madrid_bars")
plt.show()











distribuzioni=[sim_norm,sim_uni,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual
D






capacita

freq=capacita

l_sigma=np.arange(1,10,0.5)
P=[]
ms=[]
mt=[]
for i in range(20):
    PAR,min_sig,mat_sig=fun.parameter(12.5,l_sigma,capacita,df_busy,200)
    P.append(PAR)
    ms.append(min_sig)
    mt.append(mat_sig)


Pr=np.array(P)
Pr[1,0]

M=np.zeros(Pr.shape[1])
for i in range(len(M)):
    M[i]=np.mean(Pr[:,i])



plt.plot(l_sigma,M)

plt.plot(Pr.T)
plt.show()
