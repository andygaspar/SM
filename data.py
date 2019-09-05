import pandas as pd
import numpy as np
from geopy.distance import geodesic


df_ar=pd.read_csv("../data/arrivi_1709.csv")
df_wp=pd.read_csv("../data/punti_1709.csv")
df_wp.rename(columns={'astext(k.coords)':'coor'},inplace=True)

"""
    #calcolo distanza da areoporto
    AIRPORT=(50.03793, 8.56215)
    dist=geodesic(ENTRY,AIRPORT).kilometers
    dist



    # rielaborazione stringhe
    df_wp.head(100)
    type(df_wp["coor"][2])
    test=df_wp["coor"][2]
    test
    test=test.replace("POINT","")
    test=test.replace("(","")
    test=test.replace(")","")
    test
    split_test=test.split(" ")
    split_test
    split_test=[float(split_test[0]),float(split_test[1])]
    split_test=tuple(split_test)
    split_test


    #primo test su primo volo
    flight_1=df_wp['ifps_id']=="AA66960337"

    flight_1=df_wp[flight_1]
    flight_1

    #ricerca per caratteristtica, crea oggetto true false che può essere letto da df
    ar_1=df_ar['ifps_id']=="AA66960337"
    #df da oggetto true false
    ar_fl_1=df_ar[ar_1]
    ar_fl_1


    df_wp.shape
    n=flight_1=df_wp['sid']=="ODIPI"

    prova=df_wp[n]
    prova.loc[,"trajectory_id"]
    type(prova)
    prova["astext(k.coords)"]




"""








def df_coor_to_dist(df):
    AIRPORT=(50.03793, 8.56215)
    wp_dist=np.zeros(df.shape[0])
    for i in range(df.shape[0]):
        coordinate=df["coor"][i]
        coordinate=coordinate.replace("POINT","")
        coordinate=coordinate.replace("(","")
        coordinate=coordinate.replace(")","")
        split_coordinate=coordinate.split(" ")
        split_coordinate=[float(split_coordinate[0]),float(split_coordinate[1])]
        ENTRY=tuple(split_coordinate)
        dist=geodesic(ENTRY,AIRPORT).kilometers
        wp_dist[i]=dist
    #df_wp_dist.rename(columns={'coor':'distance'},inplace=True)
    return wp_dist

wp_dist=df_coor_to_dist(df_wp)
df_wp["distance"]=wp_dist
#df_wp.to_csv()


entry_condition=df_wp['distance']<200
df_entry=df_wp[entry_condition]

df_entry.to_csv()
