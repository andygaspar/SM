import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun
import data as data


def arr_hist(date,airport,index=0,BINS=24):
    """
    dato airport, data e numero bins  (BINS=default 24)
    stampa istogramma e ritorna l'array con gli arrivi
    """
    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.airport(df_ar,airport)
    arr_day=data.df_per_data(arr_day,date)
    arr_day=arr_day.sort_values(by="time_sec")
    arr_array=arr_day["time_sec"].values
    max_bin=max(arr_array)
    min_bin=min(arr_array)
    width_bin=(max_bin-min_bin)/BINS
    plt.hist(arr_array,bins=BINS, histtype='bar', ec='black')
    plt.xticks(np.arange(min_bin,max_bin, width_bin),range(0,23))
    plt.title(airport+" "+date+" "+str(index))
    plt.show()
    return arr_array


def freq_busy(start,end,date,airport):
    """
    dato ora iniziale, ora finale, data
    ritorna frequenza dei voli e df arrival con i voli nella fascia oraria
    """
    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.df_per_data(df_ar,date)
    arr_day=data.airport(arr_day,airport)
    #selezione in base al plot della fascia oraria le start-end
    cond=arr_day["time_sec"]>=start*3600
    busy_arrival=arr_day[cond]
    cond=busy_arrival["time_sec"]<end*3600
    busy_arrival=busy_arrival[cond]

    #calcolo frequenza
    if busy_arrival.shape[0]>0:
        freq=(end-start)*3600/busy_arrival.shape[0]
    else:
        freq=0
    return freq,busy_arrival



#distribuzione frequenza nelle ore della giornata
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

    plt.plot(arr_day)
    plt.plot(approx)
    plt.show()

    return curve, freq_per_h, approx




def frequenza_media(start_time,end_time,airport,lista_date):
    """
    dati start_time,end_time,airport,lista_date
    ritorna la frequenza media di quella fascia oraria
    """
    fr=0
    denom=0
    for date in lista_date:
        freq,df_arr_busy=freq_busy(start_time,end_time,date,airport)
        fr+=freq*df_arr_busy.shape[0]
        denom+=df_arr_busy.shape[0]
    if denom>0:
        return fr/denom
    else:
        return 0



def freq_analysis(airport,lista_date):
    df_ar=pd.read_csv("../data/arrivi_completo.csv")
    arr_day=data.airport(df_ar,airport)
    to_plot=np.zeros(24)
    for i in range(24):
        cond=arr_day["time_sec"]>=i*3600
        busy_arrival=arr_day[cond]
        cond=busy_arrival["time_sec"]<(i+1)*3600
        busy_arrival=busy_arrival[cond]
        to_plot[i]=busy_arrival.shape[0]
    plt.plot(range(24),to_plot/len(lista_date))
    plt.xticks(np.arange(0, 24, 1))
    plt.grid(b=True,axis='x')
    plt.title("Medie arrivi")
    plt.show()


def find_capacity(start_time, end_time, df = df_ar,lista_date = lista_date):
    """
    funzione che calcola capacita media del servizio
    INPUT:
        -start_time: lista di vettori di start_time (stessa lunghezza di end_time)
        -end_time:ista di vettori  di end_time (stessa lunghezza di start_time)
    OUTPUT:
        capacità media delle varie zone orarie date in input
    """
    cap = np.zeros(len(start_time))

    for i in range(len(start_time)):
        dfarr=data.df_per_data(df_ar,lista_date)
        dfarr=data.df_fascia_oraria(dfarr,start_time[i],end_time[i])
        capacita=3600/(dfarr.shape[0]/(len(lista_date)*(end_time[i]-start_time[i])))
        cap[i]=capacita
    capacita = sum(cap)/len(cap)
    return capacita




def find_ro(freq,start_time,end_time,lista_date,airport):
    """
    ritorna ro,max_arrival_per_h
    """
    d_ar=pd.read_csv("../data/arrivi_completo.csv")
    df_ar=data.airport(d_ar,airport)
    max=0
    for date in lista_date:
        arr_day=data.df_per_data(df_ar,date)
        arr_day=data.airport(arr_day,airport)
        for i in range(start_time,end_time):
            cond=arr_day["time_sec"]>=i*3600
            busy_arrival=arr_day[cond]
            cond=busy_arrival["time_sec"]<(i+1)*3600
            busy_arrival=busy_arrival[cond]
            if(busy_arrival.shape[0]>max):
                max=busy_arrival.shape[0]


    return (3600/freq)/max,max
