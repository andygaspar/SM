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


#ciao pippo




#caricamento preliminari
d=pd.read_csv("../data/completo.csv")
d_ar=pd.read_csv("../data/arrivi_completo.csv")



#scelta aeroporto e filtro distanze
airport="EDDF"
df_day=pd.read_csv("francoforte.csv")

lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste(airport)
lista_date.sort()
d_wp_coor=fun.dict_wp_coor(airport)
df=data.airport(d,airport)
df_ar=data.airport(d_ar,airport)
#df=data.dist_filter(df,400)


#analisi frequenze
"""
for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)
"""
aa.freq_analysis("EGLL",lista_date,"freq H")


#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)


"**********************************************"
#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=3
end_time=20


date=lista_date[6]
arr_day=data.df_per_data(df_ar,date)
arr_day=data.airport(arr_day,airport)
arr_day=arr_day.sort_values(by="time_sec")



freq_wp=fun.dict_wp_freq(airport)
freq_wp
wp_list=list(freq_wp.keys())
wp_list[:30]
#pp.bubble_plot_2(df,airport,wp_list[:30],al=0.5,scale=0.1,textsize=22)

#lista_wp=["KERAX","PSA","UNOKO","ROLIS","PESOV","NIVNU"]
#df_day,delay=data.df_finale_delay(df,df_ar,date,lista_wp)
#df_day

"*******************************simul   ****************"
wp_f=fun.dict_wp_freq("EGLL")
curve, freq_per_h, approx,pol=aa.freq_analysis_by_day(date,airport,DEG=30)

#plot frequency of arrivals
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
len(t)/(end_time-start_time)   #arrivi per ora
3600/(len(t)/(end_time-start_time))   #freq


df_busy=data.df_busy(df_day,start_time,end_time,"time_sec")
df_busy,delay=data.sort_df(df_busy)
df_busy=data.df_per_data(df_busy,date)
df_busy


#plot fitting di t
plt.plot(arr_test["time_sec"].values/3660)
plt.plot(t/3660)
#plt.savefig("aprrox_schedule")


#controllo parametri
min(approx)


#simulazione
schedule=t
sigma=40
capacita=75
data_queue=df_busy["delay"].values/capacita
#data_queue=fun.reject_outliers(data_queue)
sim,sim_matrix=ss.simulation_PSRA_M(200, schedule,capacita,sigma,"norm",True)
sim_uni,sim_matrix_uni=ss.simulation_PSRA_M(200, schedule,capacita,sigma,"uni",True)

#creazione polinomio interpolante i data_queue
pol_data=np.polyfit(np.arange(len(data_queue)),data_queue,15)
approx_d=np.polyval(pol_data,np.arange(len(data_queue)))


#rescaling grafici di confronto
x=np.array(df_busy["a_time_sec"].values)
new_x=np.arange(start_time*3600,end_time*3600,capacita)
#approx_data_to_plot=plot_interp(approx_d,x,new_x,capacita)




len(approx)

len(new_x)
len(sim)
#len(approx_data_to_plot)
new_x=np.append(new_x,new_x[-1]+capacita)
#plot frequency of arrivals
plt.plot(np.ones(len(approx))*capacita)
plt.plot(np.arange(len(approx)),approx)

plt.plot(approx_to_plot)



data_queue[data_queue>20]=0
shift=0
plt.scatter(np.arange(start_time*3600,end_time*3600,(end_time-start_time)*3600/len(approx)),3600/(approx*10),marker=".")
plt.scatter(x,data_queue,marker=".",color="grey")
plt.plot(new_x,sim,color="red")
plt.plot(new_x,sim_uni,color="green")
#plt.plot(new_x[:-1],approx_data_to_plot,color="orange")

plt.savefig("our_2")

np.mean(sim)
np.mean(sim_uni)
np.mean(data_queue)


np.var(data_queue)






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
