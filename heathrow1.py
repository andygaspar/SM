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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter






#caricamento preliminari
d=pd.read_csv("../data/completo.csv")
d_ar=pd.read_csv("../data/arrivi_completo.csv")



#scelta aeroporto e filtro distanze
airport="EGLL"


lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste(airport)
lista_date.sort()
d_wp_coor=fun.dict_wp_coor(airport)
df=data.airport(d,airport)
df_ar=data.airport(d_ar,airport)
df=data.dist_filter(df,300)










#analisi frequenze

for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)
aa.freq_analysis(airport,lista_date)





#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)


#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=7
end_time=12

#wp_f=fun.dict_wp_freq("EGLL")



#scelta waypoint
wp=["LOGAN","LAM","ALESO","BNN"]


#creazione del df_finale per wp e tutte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
df_all_days=pd.read_csv("heathrow_2.csv")
#df_all_days=pd.read_csv("heathrow.csv")
df_all_days




dfarr=data.df_per_data(df_ar,lista_date)
dfarr=data.df_fascia_oraria(dfarr,start_time,end_time)
dfarr.shape
capacita_1=3600/(dfarr.shape[0]/(len(lista_date)*(end_time-start_time)))


dfarr=data.df_per_data(df_ar,lista_date)
dfarr=data.df_fascia_oraria(dfarr,15,20)
dfarr.shape
capacita_2=3600/(dfarr.shape[0]/(len(lista_date)*(end_time-start_time)))
capacita=(capacita_1+capacita_2)/2
capacita


#df_entry_zone=data.df_lista_wp(d,["LAM","ALESO","BNN","OCK"])


#calcolo frequenza media nella fascia oraria in tutte le date scelte
#capacita=aa.frequenza_media(start_time,end_time,airport,lista_date)


#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)

df_busy_2=data.df_busy(df_all_days,15,20)
df_busy_2,delay=data.sort_df(df_busy_2)

df_busy=df_busy.append(df_busy_2)

df_busy.shape







capacita
freq=capacita

sigma=20.5
iterazioni=200
len_periodo=13
sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo ,capacita, freq,sigma)
sim_norm=ss.sim_distribution(sim_matrix)
sim,sim_matrix=ss.simulation_PSRA(iterazioni,len_periodo,capacita, freq,sigma,"uni")
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


plt.plot(sim_norm,label="simulation_NORM")
plt.plot(sim_uni,label="simulation_UNI")
#plt.plot(sim_exp,label="simulation_EXP")
#plt.plot(sim_tri,label="simulation_TRI")
plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" HEATHROW sigma="+str(sigma))
plt.legend()
plt.show()
plt.savefig("results/heatrow.png")

distribuzioni=[sim_norm,sim_uni,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual
D






capacita
freq


l_sigma=np.arange(15,25.5,0.5)
P=[]
ms=[]
mt=[]
for i in range(3):
    PAR,min_sig,mat_sig=fun.parameter(13,l_sigma,freq,capacita,df_busy,200)
    P.append(PAR)
    ms.append(min_sig)
    mt.append(mat_sig)


Pr=np.array(P)
Pr[1,0]

M=np.zeros(Pr.shape[1])
for i in range(len(M)):
    M[i]=np.mean(Pr[:,i])





for i in range(len(Pr)):
    plt.plot(np.arange(15,25.5,0.5),Pr[i],linewidth=0.5)
plt.plot(np.arange(15,25.5,0.5),M,linewidth=8)
plt.xlabel(" possible value of sigma")
plt.legend()
