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
df=data.df_per_data(df,lista_date[0])





wp=["KERAX","PSA","ROLIS","UNOKO"]
date=lista_date[0]

#vettore arrivi e istogramma,  utile al calcolo della frequenza e alla scelta del lasso temporale
arr_vect=aa.arr_hist(lista_date[0])
help(aa)
help(data)
help(fun)
help(ss)

#df completo della giornata in questione
df_delay,min_dict=data.df_finale_delay(df,df_ar,date,wp)


#calcolo frequenza e creazione del df busy
freq,df_arr_busy=aa.freq_busy(5,20,date)
freq
df_busy=data.df_busy(df_delay,5,20)
df_busy,delay=data.sort_df(df_busy)
df_busy
np.mean(delay)
np.var(delay)

plt.plot(delay)

#pulizia dagli outliers, clean sono i DATI FINALI EFFETTIVI
clean=fun.reject_outliers(delay)
plt.plot(clean/60)
np.std(clean)


# run del modello
queue, delay_sim, arr=ss.PSRA(20-5,"uni",freq,np.std(clean))



max(delay_sim)
#plot
plt.plot(clean/60,color="red")
plt.plot(delay_sim,color="blue")
plt.show()

queue
plt.plot(queue)
plt.plot(arr)
delay_sim


test=np.random.normal(0, np.std(clean)/freq, len(clean))
test1=np.random.normal(0, 20/90, len(clean))

max(clean)/60
max(test)
max(test1)


e=chisquare(clean,np.random.choice(delay_sim,len(clean)))

e
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
