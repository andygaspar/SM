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
freq_analysis(airport,lista_date)





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



plt.plot(np.arange(15,25.5,0.5),M)

plt.plot(Pr.T)
plt.show()



np.min(PAR)
np.argmin(PAR)
plt.plot(np.arange(15,25.5,0.5),PAR)

plt.plot(PAR)
PAR.shape
np.arange(5,21,0.5).shape

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

df
plt.show()
"""

df=df[~df.duplicated("aereo")]
df

start_time
arr_per_h=[]
rel_delay=[]
for date in lista_date:
    df_day=data.df_per_data(df_ar,date)
    for i in range(start_time,end_time):
        cond=df_day["time_sec"]>=i*3600
        df_aux=df_day[cond]
        cond=df_aux["time_sec"]<(i+1)*3600
        df_aux=df_aux[cond]
        arr_per_h.append(df_aux.shape[0])
        #rel_delay.append(sum(df_aux["delay"])/df_aux.shape[0])


for date in lista_date:
    df_day=data.df_per_data(df_busy,date)
    for i in range(start_time,end_time):
        cond=df_day["time_sec"]>=i*3600
        df_aux=df_day[cond]
        cond=df_aux["time_sec"]<(i+1)*3600
        df_aux=df_aux[cond]
        rel_delay.append(sum(df_aux["delay"])/df_aux.shape[0])


arr_per_h=np.array(arr_per_h)
rel_delay=np.array(rel_delay)
df_busy.shape[0]/sum(arr_per_h)

arr_per_h
type("e")==str

rel_delay
rel_delay/80
stima=arr_per_h+(rel_delay/80).astype(int)
sum(stima)/(45*len(stima))
cond=stima<45
stima=stima[cond]
stima

sum(stima)/len(stima)

(sum(arr_per_h)/(45*len(arr_per_h)))

stima
df_day=data.df_per_data(df_busy,lista_date[0])
"""
******
"""


df_nuovo = df[~df.duplicated("aereo")]






"""
*******************
"""


df
f_wp=fun.dict_wp_freq(airport)
lis_wp=["LAM","BIG","WEALD","BNN","OCK"]
cond=df["sid"]=="LAM"
df_wp=df[cond]

for wp in lis_wp[1:]:
    cond=df["sid"]==wp
    df_aux=df[cond]
    df_wp=df_wp.append(df_aux)



df_wp.shape[0]
df_wp
perc=df_wp.shape[0]/df[~df.duplicated("aereo")].shape[0]
perc


df_ok=data.df_per_data(df_wp,lista_date[0])
df_ok.shape

for date in lista_date[1:]:
    df_ok=df_ok.append(data.df_per_data(df_wp,date))

df_ok.shape
cond=df_ok["time_sec"]>=start_time*3600
df_ok=df_ok[cond]
cond=df_ok["time_sec"]<end_time*3600
df_ok=df_ok[cond]


df_ok=df_ok[~df_ok.duplicated("aereo")]



df_ok.shape
voli_entrati=df_ok.shape[0]/(28*(end_time-start_time))

voli_entrati

yyy=3600/(voli_entrati)
yyy

ro=(voli_entrati/perc)/46
ro
freq





df_test=data.df_per_data(df,lista_date[0])
df_test.shape
for date in lista_date[1:]:
    df_test=df_test.append(data.df_per_data(df,date))

df_test.shape

df_test

cond=df_test["time_sec"]>=start_time*3600
df_test=df_test[cond]
df_test.shape
cond=df_test["time_sec"]<end_time*3600
df_test=df_test[cond]
df_test.shape

df_test=df_test[~df_test.duplicated("aereo")]
df_test.shape

testdata=df_ok[~df_ok.duplicated("date")]
testdata.shape[0]

correttivo=df_ok.shape[0]/df_test.shape[0]
"LAM" in list(df_test["sid"])
