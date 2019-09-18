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

lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()


"aeroporto destinazione"
airport="EDDF"
df=data.airport(df,airport)
df_ar=data.airport(df_ar,airport)
df=data.dist_filter(df,300)



"data e wp"
wp=["KERAX","PSA","ROLIS","UNOKO"]
date=lista_date[5]
df=data.df_per_data(df,date)
df_ar=data.df_per_data(df_ar,date)
df_ar=df_ar.sort_values(by="time_sec")
df_delay,min_dict=data.df_finale_delay(df,df_ar,date,wp)




#vettore arrivi e istogramma,  utile al calcolo della frequenza e alla scelta del lasso temporale
arr_vect=aa.arr_hist(date,airport)


#definizione del periodo
start_time=2
end_time=20


#calcolo frequenza e creazione del df busy
freq,df_arr_busy=aa.freq_busy(start_time,end_time,date,airport)
df_arr_busy=df_arr_busy.sort_values(by="time_sec")
freq






#costruzione del df_finale ma solo con gli aerei del lasso temporale in esame
df_busy=data.df_busy(df_delay,start_time,end_time)
df_busy,delay=data.sort_df(df_busy)









#pudlizia dagli outliers, clean sono i DATI FINALI EFFETTIVI
clean=fun.reject_outliers(delay)
plt.plot(clean)
clean.shape




# run del modello
queue,delay_sim, arr=ss.PSRA_2(end_time-start_time,"norm",freq,10)
queue_d=plot_queues(df_busy,queue,freq)



#plot modello già convertito in delay (*freq) espresso in minuti (/60)
#plot dei delay in minuti
plt.plot(queue*freq/60)
plt.plot(df_busy["delay"].values/60)
plt.show()


#comparazione medie
np.mean(queue*freq/60)
np.mean(df_busy["delay"].values/60)

#comparazione st deviation
np.std(queue*freq/60)
np.std(df_busy["delay"].values/60)






def plot_queues(df_busy,queue,freq):
    """
    dato il df_busy e la coda simulata
    crea un array coda_da_data e i sui indici (per il plot)
    """
    df=df_busy.sort_values(by="a_time_sec")
    queue_d=np.zeros(len(queue))
    shift=min(df_busy["a_time_sec"])
    for i in range(df_busy.shape[0]):
        index=int((df_busy.iloc[i]["a_time_sec"]-shift)/freq)
        if index<len(queue):
            queue_d[index]=int(df_busy.iloc[i]["delay"]/freq)

    #interpretazione
    i=0
    while i<len(queue_d)-1:
        a=queue_d[i]
        b=0
        k=i+1
        while k<(len(queue_d)-1) and queue_d[k]==0:
            k+=1
        b=queue_d[k]
        for j in range(i+1,k):
            queue_d[j]=a+(j-i)*(b-a)/(k+1-i)
        i=k

    plt.plot(queue/60,label="simulation")
    plt.plot(queue_d/60,label="actual data")
    plt.legend()
    plt.show()

    return queue_d




queue_d=plot_queues(df_busy,queue,freq)




#test....ma ancora non vuole dire nulla e bisogna capire bene

#e=chisquare(clean,np.random.choice(delay_sim,len(clean)))


"""
"********************** programma ******************************"

ALBI

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
