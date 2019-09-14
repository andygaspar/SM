import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import arrival_analysis as aa
import data as data
import csv
import copy

df=pd.read_csv("../data/completo.csv")
df_ar=pd.read_csv("../data/arrivi_completo.csv")
df=data.dist_filter(df,300)
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()
df=data.df_per_data(df,lista_date[0])



lista_date
lista_wp
lista_freq_wp
d_wp_coor
df

aa.arr_hist(lista_date[0])


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
