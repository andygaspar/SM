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

df1=data.df_per_data(df,lista_date)
df_aux=data.df_fascia_oraria(df1,5,10)
df_aux=df_aux.append(data.df_fascia_oraria(df,12.5,18.5))
df_aux=df_aux[~df_aux.duplicated("aereo")]
df_aux.shape




help(data.df_fascia_oraria)
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

lista_date



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

df_busy.shape

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
plt.title(" FRANKFURT  with sigma-factor="+str(sigma))
plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()
plt.savefig("../Frankfurt")
plt.show()



len(data_r)
len(sim_uni)
X = np.arange(16)
#Z = np.arange(33)
plt.bar(X+0.00,sim_uni, color = 'b', width = 0.30,label = "uniform distribution")
plt.bar(X+0.30,data_r[:16], color = 'r', width = 0.30,label = "data rounded")
plt.title(" HEATHROW  with sigma-factor ="+str(sigma))
plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()
plt.savefig("../frankfurt_bar_uni")
plt.show()



len(sim_norm)
Z = np.arange(15)
#Z = np.arange(33)
plt.bar(Z+0.00,sim_norm, color = 'b', width = 0.30,label = "normal distribution")
plt.bar(Z+0.30,data_r[:15], color = 'r', width = 0.30,label = "data rounded")
plt.title(" HEATHROW  with sigma-factor ="+str(sigma))
plt.xlabel("Queue length")
plt.ylabel("Probability")
plt.legend()
plt.savefig("../frankfurt_bar_norm")
plt.show()






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
for i in range(25):
    print(i)
    PAR,min_sig,mat_sig=fun.parameter(11,l_sigma,freq,capacita,df_busy,200)
    P.append(PAR)
    ms.append(min_sig)
    mt.append(mat_sig)


 Pr=np.array(P)
M=np.zeros(Pr.shape[1])
for i in range(len(M)):
    M[i]=np.mean(Pr[:,i])

np.argmin(M)


for i in range(len(Pr)):
    plt.plot(np.arange(4,12.5,0.5),Pr[i],linewidth=0.5)
plt.plot(np.arange(4,12.5,0.5),M,linewidth=5,label = "mean plot")
plt.title("Estimation of sigma-factor")
plt.xlabel("value od sigma factor ")
plt.ylabel("quality value")
plt.legend()
plt.savefig("../frankfurt_sigmas.png")
