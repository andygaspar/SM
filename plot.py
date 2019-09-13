import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data




"""
plot utilizzo degli waypoint
"""

df_bubble=pd.read_csv("../data/completo.csv")
lista_date,lista_wp,lista_freq_wp,wp_coor=data.carica_liste()
df_bubble=data.dist_filter(df_bubble,200)
df_bubble=data.df_per_data(df_bubble,lista_date[0])

def make_coor_dict(df):
    """
    calcola le frequenze degli waypoint
    """
    waypoint=fun.frequency(df,"sid")
    N=len(waypoint)

    coor_dict={}
    for i in range(df_bubble.shape[0]):
        key=df_bubble.iloc[i]["sid"]
        if key not in coor_dict:
            coor_dict[key]=df_bubble.iloc[i]["coor"]

    return coor_dict
#vettore x

def bubble_plot(df,coor_dict,wp_list,al=0.5,scale=0.1):
    N=len(coor_dict)
    x=np.zeros(N)
    y=np.zeros(N)
    z=np.zeros(N)
    i=0
    fr_dict=fun.frequency(df,"sid")
    for key in coor_dict:
        c=fun.coord(coor_dict[key])
        x[i]=c[0]
        y[i]=c[1]
        z[i]=fr_dict[key]
        i=i+1
    #plt.figure(figsize=(20,15))
    plt.scatter(y,x ,s=z*0.3, alpha=al)
    lon=8.560964
    lat=50.037753
    plt.scatter( lon,lat,color="red")
    plt.annotate("FR",xy=(lat,lon),xytext=(lat-0.15, lon-0.15))
    for wp in wp_list:
        c=fun.coord(coor_dict[wp])
        plt.scatter(c[1],c[0],color="green")
        plt.annotate(wp,xy=(c[1],c[0]),xytext=(c[1]-0.15, c[0]-0.15))

    plt.show()


coor_dict=make_coor_dict(df_bubble)
coor_dict
wp_list=["KERAX","PSA","ROLIS","UNOKO"]
fr_dict=fun.frequency(df_bubble,"sid")
fr_dict
fr=list(fr_dict.keys())
fr=[x for x in fr if x not in wp_list]
fr[0:20]
bubble_plot(df_bubble,coor_dict,wp_list+fr[0:10],scale=0.3)

coor_dict["UNOKO"]
