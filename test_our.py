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

for i in range(len(lista_date)):
    arr_vect=aa.arr_hist(lista_date[i],airport,i,24)

aa.freq_analysis("EGLL",lista_date,"freq H")


#tolto il primo giorno perché inutile come si vede dai grafici
lista_date.pop(0)
lista_date.pop(-1)


"**********************************************"
#scelta lasso lasso_temporale_in_ore in base all'analisi dei grafici
start_time=3
end_time=19


date=lista_date[1]
arr_day=data.df_per_data(df_ar,date)
arr_day=data.airport(arr_day,airport)
arr_day=arr_day.sort_values(by="time_sec")



freq_wp=fun.dict_wp_freq(airport)
wp_list=list(freq_wp.keys())
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
plt.figure(figsize=(15,10))
plt.rc("axes",titlesize=30)
plt.rc("font",size=25)
plt.plot(np.arange(len(t[:-3])),arr_test["time_sec"].values/3600,label="actual")
plt.plot(np.arange(len(t[:-3])),t[:-3]/3600,label="aprrox schedule")
plt.title("Flight - arrival time")
plt.legend()
#plt.savefig("../Plot/approx_arrival.png")
#plt.savefig("aprrox_schedule")


#controllo parametri
min(approx)


#simulazione
schedule=t
sigma=20
capacita=60
data_queue=df_busy["delay"].values/capacita
#data_queue=fun.reject_outliers(data_queue)
sim,sim_matrix=ss.simulation_PSRA_M(200, schedule,capacita,sigma,"norm",False)
sim_uni,sim_matrix_uni=ss.simulation_PSRA_M(200, schedule,capacita,sigma,"uni",False)




#rescaling grafici di confronto
x=np.array(df_busy["a_time_sec"].values)
new_x=np.arange(start_time*3600,end_time*3600,capacita)
#approx_data_to_plot=plot_interp(approx_d,x,new_x,capacita)


len(new_x)
len(sim)
#len(approx_data_to_plot)
new_x=np.append(new_x,new_x[-1]+capacita)
#plot fr



data_queue[data_queue>20]=0
shift=0
plt.figure(figsize=(15,10))
plt.rc("axes",titlesize=30)
plt.rc("font",size=25)
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






#creazione polinomio interpolante i data_queue
pol_data=np.polyfit(np.arange(len(data_queue)),data_queue,15)
approx_d=np.polyval(pol_data,np.arange(len(data_queue)))





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





def freq_analysis_by_day(date,airport,DEG=30):
    """
    data una data e un aeroporto
    restituisce:
        un vettore con tutte le frequenze inter arrival
        un vettore con le frequenze medie per ora
        un vettore con la curva che approx l'andamento della frequenza
            mediande i minimi quadrati con un pol di ordine DEG=30
    """

    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.df_per_data(df_ar,date)
    arr_day=data.airport(arr_day,airport)
    arr_day=arr_day.sort_values(by="time_sec")

    curve=np.zeros(arr_day.shape[0]-1)

    for i in range(arr_day.shape[0]-1):
        curve[i]=arr_day.iloc[i+1]["time_sec"]-arr_day.iloc[i]["time_sec"]


    freq_per_h=np.zeros(24)
    j=0
    for i in range(24):
        k=j
        while k<arr_day.shape[0] and arr_day.iloc[k]["time_sec"]<(i+1)*3600:
            k+=1
        if k>j+1:
            freq_per_h[i]=np.mean(curve[j:k+1])
        j=k

    pol=np.polyfit(arr_day["time_sec"].values[0:-1],curve,DEG)
    approx=np.polyval(pol,arr_day["time_sec"].values[0:-1])

    plt.figure(figsize=(15,10))
    plt.rc("axes",titlesize=30)
    plt.rc("font",size=20)

    plt.plot(arr_day["time_sec"].values[0:-1]/3600,curve,label="Actual interarrival time")
    plt.plot(arr_day["time_sec"].values[0:-1]/3600,approx,label="MS approx DEG="+str(DEG),linewidth=3)

    plt.legend()
    plt.title("Inter-arrival approximation")
    plt.savefig("../Plot/freq_approx.png")
    plt.show()

    return curve, freq_per_h, approx, pol
