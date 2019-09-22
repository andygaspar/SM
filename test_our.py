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
import plot as pp
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter






#caricamento preliminari
d=pd.read_csv("../data/completo.csv")
d_ar=pd.read_csv("../data/arrivi_completo.csv")



#scelta aeroporto e filtro distanze
airport="EDDF"
df_all_days=pd.read_csv("francoforte.csv")

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
aa.freq_analysis(airport,lista_date)


#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)


"**********************************************"
#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=4
end_time=18


date=lista_date[4]
arr_day=data.df_per_data(df_ar,date)
arr_day=data.airport(arr_day,airport)
arr_day=arr_day.sort_values(by="time_sec")




"*******************************simul   ****************"
#wp_f=fun.dict_wp_freq("EGLL")
curve, freq_per_h, approx,pol=aa.freq_analysis_by_day(date,airport,DEG=30)

plt.plot(arr_day["time_sec"].values[0:-1]/3600,curve)
plt.plot(arr_day["time_sec"].values[0:-1]/3600,approx)
plt.plot(3600/approx[20:-20])

t=[]
t.append(start_time*3600)
while t[-1]<end_time*3600:
    t.append(t[-1]+np.polyval(pol,t[-1]))
t=np.array(t)



arr_test=arr_day[arr_day["time_sec"]>=start_time*3600]
arr_test=arr_test[arr_test["time_sec"]<end_time*3600]
arr_test.shape
len(t)
len(t)/12   #arrivi per ora
3600/(len(t)/(end_time-start_time))   #freq



df_busy=data.df_busy(df_all_days,start_time,end_time,"time_sec")
df_busy,delay=data.sort_df(df_busy)
df_busy=data.df_per_data(df_busy,date)
df_busy

"""
plt.plot(np.arange(len(df_busy["a_time_sec"].values))*len(arrival)/len(df_busy["a_time_sec"].values),df_busy["a_time_sec"].values)
plt.plot(sorted(arrival))
"""
plt.plot(arr_test["time_sec"].values/3660)
plt.plot(t/3660)






min(approx)
schedule=t
sigma=100
capacita=65
data_queue=df_busy["delay"].values/capacita
data_queue=fun.reject_outliers(data_queue)
sim,sim_matrix=simulation_PSRA_M(200, schedule,capacita,sigma,"norm",False)
sim_uni,sim_matrix_uni=simulation_PSRA_M(200, schedule,capacita,sigma,"uni",False)

pol_data=np.polyfit(np.arange(len(data_queue)),data_queue,20)
approx_d=np.polyval(pol_data,np.arange(len(data_queue)))


x=np.array(df_busy["a_time_sec"].values)
new_x=np.arange(start_time*3600,end_time*3600,capacita)
approx_to_plot=plot_interp(approx_d,x,new_x,capacita)
queue_to_plot=plot_interp(data_queue,x,new_x,capacita)

plt.plot(3600/approx[20:-20])


plt.plot(queue_to_plot)
plt.plot(approx_to_plot)
plt.plot(sim,color="red")
plt.plot(sim_uni,color="pink")
plt.show()


np.mean(sim)
np.mean(data_queue)


def plot_interp(f_x,x,new_x,step):
    """
    dato il df_busy e la coda simulata
    crea un array coda_da_data e i sui indici (per il plot)

    poi plotta
    """
    new_fx=np.zeros(len(new_x))-1
    shift=min(new_x)
    for i in range(len(f_x)):
        index=int((x[i]-shift)/step)
        new_fx[index]=f_x[i]

    #interpolazione

    i=0
    while i<len(new_fx)-1:
        a=new_fx[i]
        b=0
        k=i+1
        while k<(len(new_fx)-1) and new_fx[k]==-1:
            k+=1
        b=new_fx[k]
        for j in range(i+1,k):
            new_fx[j]=a+(j-i)*(b-a)/(k+1-i)
        i=k

    return abs(new_fx)


















"costruzione della funzione arrivi"
def arr_m(schedule,capacita,f,fattore_sigma,negative_delays):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """
    lam=1/capacita
    delay=np.zeros(len(schedule))

    #casi distribuzioni
    # if f=="exp":
        # delay=np.array(samp.sample_from_exp(lam/fattore_sigma,len(schedule)))-fattore_sigma/lam

    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        delay=np.random.uniform(-int_a_b,int_a_b,len(schedule))
        if negative_delays==False:

            #delay[delay<0]=0
            delay[delay<0]=abs(delay[delay<0])


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, len(schedule))
        if negative_delays==False:
            #delay[delay<0]=0
            delay[delay<0]=abs(delay[delay<0])

        # if f=="tri":
    # b = (fattore_sigma/lam)*np.sqrt(6)
        # delay = np.random.triangular(0,b/2,b,len(schedule))

    #calolo arrival
    arrival=np.zeros(len(schedule))

    for i in range(len(schedule)):
        arrival[i]=schedule[i] + int(delay[i])

    return arrival,delay





"costruzione PSRA_m"
def PSRA_M(schedule,distributione,capacita,sigma=20, negative_delays=True):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    N=int((schedule[-1]-schedule[0])/capacita)
    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr_m(schedule,capacita,distributione,sigma,negative_delays)

    #costruzione del PSRA
    queue=np.zeros(N)
    #queue_old=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=capacita*(i-1)+schedule[0]) & (arrival<capacita*i+schedule[0])])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)


    return queue,delay,arrival




"****************   simulazioni  *******************************"



def simulation_PSRA_M(N, schedule,capacita,sigma, distrib="norm",negative_delays=True):
    """
    dato N numero di simulazioni
    ritorna un vettore con l'andamento medio delle simul (stady state distr)
    """
    M=int((schedule[-1]-schedule[0])/capacita)
    sim_matrix=np.zeros((N,M))
    sim=np.zeros(M)
    for i in range(N):
        sim_matrix[i],x,y=PSRA_M(schedule,distrib,capacita,sigma,negative_delays)
    for i in range(M):
        sim[i]=np.mean(sim_matrix[:,i])

    return sim,sim_matrix








#scelta waypoint
wp=["LOGAN","LAM","ALESO","BNN"]


#creazione del df_finale per wp e tutte le date nella lista (molto lento!!!!!!!)
#df_all_days=data.df_finale_delay_multidata(df,df_ar,wp,lista_date)
df_all_days=pd.read_csv("heathrow_2.csv")
#df_all_days=pd.read_csv("heathrow.csv")

d=data.df_per_data(df,lista_date)
dd=data.df_fascia_oraria(d,start_time,end_time)
dd=dd[~dd.duplicated("aereo")]
dd.shape


tutti=df[~df.duplicated("aereo")]
tutti.shape

df_entry_zone=data.df_lista_wp(d,["LAM","ALESO","BNN","OCK"])
df_entry_zone=data.df_fascia_oraria(df_entry_zone,start_time,end_time)
df_entry_zone.shape[0]
3600/(dd.shape[0]/(len(lista_date)*(end_time-start_time)))

#calcolo frequenza media nella fascia oraria in tutte le date scelte
capacita=aa.frequenza_media(start_time,end_time,airport,lista_date)


#df_finale filtrato con solo la fascia oraria di interesse
df_busy=data.df_busy(df_all_days,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)


df_busy.shape






ro,max_cap=aa.find_ro(freq,start_time,end_time,lista_date,airport)
ro

80/0.976
freq
fattore=90/(3600/(0.976*41))

capacita
freq=yyy
freq=87.9

sigma=20
iterazioni=200
len_periodo=6
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
#plt.plot(data_t,label="data truncated")
plt.plot(data_r,label="data rounded")
plt.title(" HEATHROW sigma="+str(sigma))
plt.legend()
plt.show()

distribuzioni=[sim_norm,sim_uni,data_t,data_r]
distrib=fun.standardise_len(distribuzioni)
D=fun.dist_mat(distrib)
qual=fun.quality(D)
qual

distrib
D





capacita=80/ro


l_sigma=np.arange(15,31,2)
PAR,min_sig,mat_sig=fun.parameter(50,l_sigma,freq,capacita,df_busy,100)

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
