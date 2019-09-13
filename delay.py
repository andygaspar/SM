


def df_finale(df,df_ar,date,lista_waypoint):

    """
    dati df entrate e arrivi, una data, e una lista di wp
    ritorna un df con il tempo di arrivo e il flytime
    """
    lista_wp=copy.deepcopy(lista_waypoint)
    df_day=data.df_per_data(df,date)
    df_new=df_lista_wp(df_day,lista_wp)
    a=[]
    ta=[]
    tv=[]
    for i in range(df_new.shape[0]):
        cond=df_ar["aereo"]==df_new.iloc[i]["aereo"]
        aux=df_ar[cond]
        a.append(aux["time"].values[0])
        ta.append(aux["time_sec"].values[0])
        tv.append(ta[i]-df_new.iloc[i]["time_sec"])

    df_new["a_time"]=a
    df_new["a_time_sec"]=ta
    df_new["fly time"]=tv

    return df_new

def df_finale_delay(df,df_ar,date,lista_waypoint):
    """
    uguale a df dinale solo con l'aggiunta del delay
    ritorna df finale e un dict con i tempi minimi di percorrenza di ciascun wp
    """
    df_delay=df_finale(df,df_ar,date,lista_waypoint)
    delay_dict=fun.min_time_dict(df_delay,lista_waypoint)
    delay=np.zeros(df_delay.shape[0])
    for i in range(df_delay.shape[0]):
        delay[i]=df_delay.iloc[i]["fly time"]-delay_dict[df_delay.iloc[i]["sid"]]

    df_delay["delay"]=delay
    return df_delay,delay_dict




"********************** programma ******************************"
l=lista_wp[0:3]
d=lista_date[0]
l
df_uno,min_dict=df_finale_delay(df,df_ar,d,l)
df_uno
min_dict


df_ordinato=df_uno.sort_values(by="a_time_sec")
df_ordinato
delay=df_ordinato["delay"].values

np.mean(delay)
plt.plot(delay/60)
