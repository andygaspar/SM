import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data
import csv
import copy




df=pd.read_csv("../data/completo.csv")
df=data.dist_filter(df,200)
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
d_wp_coor=fun.dict_wp_coor()
df=data.df_per_data(df,lista_date[0])
df

main=["KERAX","PSA","ROLIS","UNOKO"]

trajectory=fun.traiettorie_complete(df)



scaled_long,scaled_lat=fun.shift_coor(d_wp_coor)
plt.scatter(scaled_long,scaled_lat)
