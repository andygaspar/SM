import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data




"""
plot utilizzo degli waypoint
"""



def freq_list_to_plot(df,num_more_freq,additional_list):
    """
    dato un df,  il numero di wp più frequenti che si vuole ottenere
    (e opzionale una lista di punti da aggiungere alla lista cmq)
    ritorna la lista voluta
    """
    fr_dict=fun.dict_wp_freq()
    fr=list(fr_dict.keys())
    fr=[x for x in fr if x not in additional_list]
    fr=fr[0:num_more_freq]
    return fr+additional_list




def bubble_plot(df,wp_list,al=0.5,scale=0.1,textsize=22):
    """
    dato un df una lista di punti ()
    ritorna il bubble plot
    """
    """
    dato un df una lista di punti ()
    ritorna il bubble plot
    """
    coor_dict=fun.dict_wp_coor()
    N=len(wp_list)
    x=np.zeros(N)
    y=np.zeros(N)
    z=np.zeros(N)
    i=0
    fr_dict=fun.dict_wp_freq()
    for key in wp_list:
        c=fun.coord(coor_dict[key])
        x[i]=c[0]
        y[i]=c[1]
        z[i]=fr_dict[key]
        i=i+1
    plt.figure(figsize=(20,15))
    #plt.scatter(y,x ,s=z*0.3, alpha=al)
    lon=8.560964
    lat=50.037753
    AIR="FR AIRPORT"
    plt.scatter( lon,lat,color="red",s=150)
    plt.annotate(AIR,xy=(lon,lat),xytext=(lon-0.3, lat-0.1),size=textsize+1)
    for wp in wp_list:
        c=fun.coord(coor_dict[wp])
        plt.scatter(c[1],c[0],color="green")
        plt.annotate(wp,xy=(c[1],c[0]),xytext=(c[1]-0.08, c[0]-0.08),size=textsize)


    plt.show()




def bubble_plot_2(df,airport,wp_list,al=0.5,scale=0.1,textsize=22):
    """
    dato un df una lista di punti ()
    ritorna il bubble plot con bubble size
    """
    coor_dict=fun.dict_wp_coor(airport)
    N=len(wp_list)
    x=np.zeros(N)
    y=np.zeros(N)
    z=np.zeros(N)
    i=0
    fr_dict=fun.dict_wp_freq(airport)
    for key in wp_list:
        c=fun.coord(coor_dict[key])
        x[i]=c[0]
        y[i]=c[1]
        z[i]=fr_dict[key]
        i=i+1
    plt.figure(figsize=(20,15))
    plt.scatter(y,x ,s=z*0.4, alpha=al)
    lon=8.560964
    lat=50.037753
    AIR="FR AIRPORT"
    plt.scatter( lon,lat,color="red",s=150)
    plt.annotate(AIR,xy=(lon,lat),xytext=(lon-0.3, lat-0.1),size=textsize+1)
    for wp in wp_list:
        c=fun.coord(coor_dict[wp])
        plt.annotate(wp,xy=(c[1],c[0]),xytext=(c[1]-0.1, c[0]-0.1),size=textsize)

    plt.show()



def plot_queues(df_busy,queue,freq):
    """
    dato il df_busy e la coda simulata
    crea un array coda_da_data e i sui indici (per il plot)

    poi plotta
    """
    df=df_busy.sort_values(by="a_time_sec")
    queue_d=np.zeros(len(queue))
    shift=min(df_busy["a_time_sec"])
    for i in range(df_busy.shape[0]):
        index=int((df_busy.iloc[i]["a_time_sec"]-shift)/freq)
        if index<len(queue):
            queue_d[index]=int(df_busy.iloc[i]["delay"]/freq)

    #interpolazione
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
