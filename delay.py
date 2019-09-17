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

df=pd.read_csv("../data/completo.csv")
df_ar=pd.read_csv("../data/arrivi_completo.csv")
df=data.dist_filter(df,300)
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()



fff=pd.read_csv("../data/punti_1709.csv")
fff

#data e wp
wp=["KERAX","PSA","ROLIS","UNOKO"]
date=lista_date[0]
date
df=data.df_per_data(df,date)

#vettore arrivi e istogramma,  utile al calcolo della frequenza e alla scelta del lasso temporale
arr_vect=aa.arr_hist(date)


#df completo della giornata in questione
df_delay,min_dict=data.df_finale_delay(df,df_ar,date,wp)


#calcolo frequenza e creazione del df busy
freq,df_arr_busy=aa.freq_busy(5,20,date)
df_arr_busy=df_arr_busy.sort_values(by="time_sec")



df_busy=data.df_busy(df_delay,5,20)
df_busy,delay=data.sort_df(df_busy)

df_busy

plt.plot(df_busy["time_sec"].values/70000)
plt.plot(df_busy["delay"].values/4000)






#pulizia dagli outliers, clean sono i DATI FINALI EFFETTIVI
clean=fun.reject_outliers(delay)
plt.plot(clean/60)


# run del modello
queue,delay_sim, arr=ss.PSRA(20-5,"norm",freq,40)



plt.plot(df_busy["a_time_sec"].values)
plt.plot(df_busy["delay"].values)





def make_queue_from_data(df_busy,queue):
    """
    dato il df_busy e la coda simulata
    crea un array coda_da_data e i sui indici (per il plot)
    """
    queue_d=np.zeros(len(queue))
    shift=min(df_busy["time_sec"])
    queue_index=np.zeros(len(queue))
    for i in range(df_busy.shape[0]):
        index=int((df_busy.iloc[i]["time_sec"]-shift)/30)
        if index<len(queue):
            queue_d[index]=int(df_busy.iloc[i]["delay"]/30)
            queue_index[i]=index
    cond=queue_d!=0
    queue_d=queue_d[cond]
    queue_index=queue_index[cond]

    return queue_d,queue_index

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
