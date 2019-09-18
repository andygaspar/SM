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

df=pd.read_csv("../data/punti_1709.csv")
df_ar=pd.read_csv("../data/arrivi_1709.csv")

lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()

df
"aeroporto destinazione"
airport="EDDF"
df=data.airport(df,airport)
df_ar=data.airport(df_ar,airport)
data.rinomina(df,"astext(k.coords)","coor")
data.rinomina(df,"ifps_id","aereo")
data.rinomina(df_ar,"ifps_id","aereo")
data.add_time_in_sec(df)
data.add_dist(df)
df = data.data_time(df)
data.taglio_colonne(df,["trajectory_id","geopoint_id","O","ac_id"])
data.taglio_colonne(df,["time_over"])
df=data.dist_filter(df,300)
df_ar
df
df_ar = data.data_time(df_ar,"arr_time")
data.add_time_in_sec(df_ar)
data.add_time_in_sec(df)
"data e wp"
wp=["KERAX","PSA","ROLIS","UNOKO"]
date="2017-08-17"
df=data.df_per_data(df,date)
df_ar=data.df_per_data(df_ar,date)
data.taglio_colonne(df_ar,["O","arr_time"])
df_ar=df_ar.sort_values(by="time_sec")
df_delay,min_dict=data.df_finale_delay(df,df_ar,date,wp)

data.save_df(df,"../data/completo.csv")
data.save_df(df_ar,"../data/arrivi_completo.csv")
df=pd.read_csv("../data/completo.csv")
df_ar=pd.read_csv("../data/arrivi_completo.csv")



"""
************************PROVO A SIMULARE**************************
"""
df_delay
arr_vect=aa.arr_hist(date,airport)
arr_vect
#considero solo le ore dalle 3 alle 22
freq,df_arr_busy=aa.freq_busy(3,10,date,airport)
freq
df_arr_busy=df_arr_busy.sort_values(by="time_sec")


"""
************************************************************************
"""
"""
    ESPERIMENTO--> PROVO A SCRIVERE FUNZIONE CHE FACCIA CODA UTILIZZANDO I DATI
"""
"""
***************************************************************************
"""

def coda_dai_dati(df = df_arr_busy, factor = freq):
    w = df.iloc[0]["time_sec"]

    for i in range(df.shape[0]):
        df.iloc[i]["time_sec"] = df.iloc[0]["time_sec"]
    print(df)
    service_time = 1/factor
    queue_aircraft = []
    max_seconds = df.iloc[df.shape[0]-1]["time_sec"]
    sim_time = df.iloc[0]["time_sec"]# simulation time
    t_1 = df.iloc[0]["time_sec"] # time for next event (arrival)
    t_2 = max_seconds # time for next event (departure)
    t_n = 0.0 #last event time--> tempo dell'ultimo avvenimento generico
    aircraft = 0
    t_b = 0.0 # last start of busy time--> tempo in cui la queue inizia ad essere non vuota per l'ultima volta
    i = 1
    while(sim_time<max_seconds and i<df.shape[0]):
        print("***********************")
        print("SITUAZIONE ALL' ",i," esimo giro")
        print("arrival_time",t_1)
        print("service_time",t_2)
        if(t_1<t_2): #event1:arrival
                print("ORA ARRIVO")
                sim_time = t_1
                aircraft += 1
                queue_aircraft.append(aircraft)
                t_n = sim_time
                print("i: ",i)
                print("dove sono")
                print(df.iloc[i]["time_sec"])
                t_1 =  df.iloc[i]["time_sec"]
                print(t_1)
                i = i+1
                if(aircraft==1):
                    print("entro qua!!!!!!")
                    t_b = sim_time
                    t_2 = sim_time + 1/service_time
        else:
                print("ORA SERVO!!")
                sim_time = t_2
                aircraft = aircraft -1
                queue_aircraft.append(aircraft)
                t_n = sim_time
                if(aircraft>0):
                    t_2=sim_time + 1/service_time
                else:
                    t_2 = max_seconds

    return queue_aircraft

"""
************************************************************************
"""
"""
    FINE ESPERIMENTO--> PROVO A SCRIVERE FUNZIONE CHE FACCIA CODA UTILIZZANDO I DATI 
"""
"""
***************************************************************************
"""





df_delay
#vettore arrivi e istogramma,  utile al calcolo della frequenza e alla scelta del lasso temporale
arr_vect=aa.arr_hist(date,airport)


df



#calcolo frequenza e creazione del df busy
freq,df_arr_busy=aa.freq_busy(2,21,date,airport)
df_arr_busy=df_arr_busy.sort_values(by="time_sec")
start_time=2
end_time=21



df_busy=data.df_busy(df_delay,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)

df_busy.shape

plt.plot(df_busy["time_sec"].values/70000)
plt.plot(df_busy["delay"].values)






#pulizia dagli outliers, clean sono i DATI FINALI EFFETTIVI
clean=fun.reject_outliers(delay)
plt.plot(clean)
clean.shape




# run del modello
queue,delay_sim, arr=ss.PSRA(end_time-start_time,"norm",freq,40)

#plot modello
plt.plot(queue)

plt.plot(df_busy["a_time_sec"].values)
plt.plot(df_busy["delay"].values)






queue_d,queue_index=make_queue_from_data(df_busy,queue)

#plot
plt.plot(np.linspace(0,len(queue),len(queue)),queue)
plt.plot(queue_index,queue_d)

















plt.plot(np.random.choice(delay_sim,len(clean)),label="delay_sim")
plt.plot(delay,label="clean")
plt.legend()
plt.show()



e=chisquare(clean,np.random.choice(delay_sim,len(clean)))


"""
"********************** programma ******************************"

l=["KERAX","PSA","ROLIS","UNOKO"]
d=lista_date[0]
df_uno,min_dict=df_finale_delay(df,df_ar,d,l)
df_uno,delay=sort_df(df_uno)
np.mean(delay)

#df_uno.iloc[np.argmax(delay)]["aereo"]  #max delay

plt.plot(delay/60,color="red")
p=plt.hist(df_uno["a_time_sec"].values,bins=24)
plt.show()


"""























"""
controllo traiettorie ritardatari eccessivi


cond=df["aereo"]==df_uno.iloc[np.argmax(delay)]["aereo"]
df_max_delay=df[cond]


cond=df["sid"]=="PSA"
ggg=df[cond]
ggg
df_max_delay
AA67325474
AA67325474


df_base=pd.read_csv("../data/punti_1709.csv")
cond=df_base['ifps_id']==df_uno.iloc[np.argmax(delay)]["aereo"]
df_max_delay_base=df_base[cond]
df_max_delay_base
"""



"""
test sporcizia dati

#ddd=pd.read_csv("../data/punti_1709.csv")
#ddd.iloc[180080:180110]
"""
