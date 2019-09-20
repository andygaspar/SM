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
"""
for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)
aa.freq_analysis(airport,lista_date)
"""

#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)
len(lista_date)




#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=15
end_time=21

#wp_f=fun.dict_wp_freq("EGLL")



#scelta waypoint
wp=["LOGAN","LAM","ALESO","NUGRA"]


#creazione del df_finale per wp e tutte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
df_all_days=pd.read_csv("heathrow.csv")


#calcolo frequenza media nella fascia oraria in tutte le date scelte
capacita=aa.frequenza_media(start_time,end_time,airport,lista_date)



#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)

ro,max_ro=aa.find_ro(capacita,start_time,end_time,lista_date,airport)


freq=3600/(ro*max_ro)


sigma=20
iterazioni=5000
len_periodo=50
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

#plotting
plt.plot(sim_norm,label="simulation_NORM")
plt.plot(sim_uni,label="simulation_UNI")
#plt.plot(sim_exp,label="simulation_EXP")
#plt.plot(sim_tri,label="simulation_TRI")
#plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" HEATHROW sigma="+str(sigma)+" noise="+str(noise))
plt.legend()
plt.show()

distribuzioni=[sim_norm,sim_uni,sim_exp,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual

distrib
D





capacita=80/ro

PAR,min_sig=fun.parameter(start_time,end_time,freq,capacita,df_busy,1000,noise=False)

np.min(PAR)
np.argmin(PAR)
plt.plot(np.arange(5,21,0.5),PAR)

min_sig







PAR[10,1]

int(index/PAR.shape[1])



index=np.argmin(PAR)
PAR[int(index/PAR.shape[1]),int(index)%PAR.shape[1]]
index
int(index/PAR.shape[1])
index%PAR.shape[1]

l_sigma=np.arange(5,31,2.5)
l_noise=np.arange(0,0.21,0.025)

l_sigma[int(index/PAR.shape[1])]
l_noise[index%PAR.shape[1]]





PAR.T.shape

fig=plt.figure()
ax=fig.gca(projection="3d")

x,y=np.meshgrid(l_noise,l_sigma)
ax.plot_surface(y,x,PAR)
plt.show()
x.shape
PAR.shape
y.shape

"""

label=["sim_norm","sim_uni","sim_exp","data_t","data_r"]
label
plt.axis('off')
p=plt.table(cellText=T,colLabels=label,rowLabels=label,loc='best')


plt.show()
"""
