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
"""


#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)
len(lista_date)
aa.freq_analysis(airport,lista_date)



#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=15
end_time=20

wp_f=fun.dict_wp_freq("EGLL")
wp_f


#scelta waypoint
wp=["LOGAN","LAM","ALESO","BNN"]

#creazione del df_finale per wp e tutte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
df_all_days=pd.read_csv("heathrow_1.csv")
#data.save_df(df_all_days,"heathrow_1.csv")

df_all_days



#calcolo frequenza media nella fascia oraria in tutte le date scelte
freq=aa.frequenza_media(start_time,end_time,airport,lista_date)
freq


#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy_1=data.df_busy(df_all_days,6,12.5)
df_busy=df_busy.append(df_busy_1)
df_busy,delay=data.sort_df(df_busy)
df_busy





freq

capacita=freq

sigma=13
noise=0.003
iterazioni=400
sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, 6, 20, freq,sigma, noise)
sim_norm=ss.sim_distribution(sim_matrix)
sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, 6, 20, freq,sigma, noise,"uni")
sim_uni=ss.sim_distribution(sim_matrix)
#sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"exp")
#sim_exp=ss.sim_distribution(sim_matrix)
#sim,sim_matrix=ss.simulation_PSRA(iterazioni,capacita, start_time, end_time, freq,sigma, noise,"tri")
#sim_tri=ss.sim_distribution(sim_matrix)

plt.bar(range(len(sim_uni)),sim_uni)
plt.plot(sim)
#calcolo delle code dai dati e della distribuzione relativa
#due metodi, truncated e rounded. questo perché
#delay/capacità=queue è decimale e va reso intero
data_queue_truncated=data.make_data_queue(df_busy,capacita)
data_queue_rounded=data.make_data_queue(df_busy,capacita,"rounded")
data_t=ss.data_distribution(data_queue_truncated)
data_r=ss.data_distribution(data_queue_rounded)

5*90/60

#plotting

plt.plot(sim_norm,label="simulation_NORM")
plt.plot(sim_uni,label="simulation_UNI")
#plt.plot(sim_exp,label="simulation_EXP")
#plt.plot(sim_tri,label="simulation_TRI")
plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" HEATHROW sigma="+str(sigma)+" noise="+str(noise))
plt.legend()
plt.show()

distribuzioni=[sim_norm,sim_uni,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual

distrib
D




l_sigma=np.arange(5,26,0.5)
l_noise=np.arange(0,0.21,0.005)
iterazioni=100
PAR=fun.parameter(6,20,freq,capacita,df_busy,iterazioni,l_sigma,True,l_noise)

np.min(PAR)
np.argmin(PAR)
plt.plot(PAR)

PAR=[]
with open('matrix_DB_PLOT.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        PAR.append(row)


PAR=np.array(PAR).astype(float)
PAR[1,1]

fig=plt.figure()
ax=fig.gca(projection="3d")
x,y=np.meshgrid(l_noise,l_sigma)
surf=ax.plot_surface(y,x,PAR,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

plt.imshow(PAR)
l_sigma[np.argmin(PAR)%len(l_noise)]
l_noise[int(np.argmin(PAR)/len(l_noise))]

PAR[]
len(l_sigma)
len(l_noise)
