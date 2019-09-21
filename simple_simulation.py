import sampling as samp
import numpy as np
import matplotlib.pyplot as plt
import pandas
import copy
import random as rm







"costruzione della funzione arrivi"
def arr(N,f,lam,fattore_sigma=20):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """

    lam=1/lam
    delay=np.zeros(N)



    #caso exp
    if f=="exp":
        delay=np.array(samp.sample_from_exp(lam/fattore_sigma,N))


    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        delay=np.random.uniform(-int_a_b,int_a_b,N)
        #delay[delay<0]=0


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, N)
        #delay[delay<0]=0

    if f=="tri":
        b = (20/lam)*np.sqrt(6)
        delay = np.random.triangular(0,b/2,b,N)




    #calolo arrival
    arrival=np.zeros(N)

    for i in range(N):
        arrival[i]=i/lam + int(delay[i])

    return arrival,delay



"costruzione PSRA"
def PSRA(lasso_temporale_in_ore,distributione,lam,fattore_sigma):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    N=int(T/lam)

    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr(N,distributione,lam,fattore_sigma)


    #costruzione del PSRA
    queue=np.zeros(N)
    #queue_old=np.zeros(N)
    for i in range(1,N):

        arrival_in_slot=len(arrival[(arrival>=lam*(i-1)) & (arrival<lam*i)])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)



    return queue,delay,arrival
"""""
ORA--> VOGLIO FARE SIMULAZIONI CON IL PSRA E VEDERE A LUNGO ANDARE SE LA DISTRIBUZIONE
DELLA QUEUE DIPENDE O MENO DALLA DISTRIBUZIONE DEL RITARDO.

"""""

def create_distribution(vector):
    """
    funzione che serve per creare una distribuzione di probabilità sui numeri
    contenuti dentro il vettore
    esempio dato v = [0,1,2,2,2,1,0,3] allora il risultato sarà res = [2/8,2/8,3/8,1/8]
    INPUT: vettore di interi sottoforma di lista
    OUTPUT: distribuzione discreta di probabilità
    """
    res = []
    N = len(vector)
    vector_np = np.array(vector)
    massimo = np.max(vector)
    for i in range(int(massimo+1)):
        cont = 0
        for j in range(len(vector)):
            if vector[j]==i:
                cont+=1
        res.append(cont/N)

    return res



def trovo_massimo(lista):
    """
    dta una lista ti trova il massimo
    """
    v = []
    for i in range(len(lista)):
         v.append(len(lista[i]))
    v = np.array(v)
    return np.max(v)

def media_vettori(lista):
    """
    data una lista di lista, ti trova la media component-wise delle liste contenute
    nella lista (ritorna uuna lista)
    INPUT: lista di liste
    OUTPUT: lista con le medie

    """
    res = []
    N = len(lista)
    n = trovo_massimo(lista)
    #trasformo tutti i vettori con la stessa dimensione
    for i in range(len(lista)):
        temp = lista[i]
        if(len(temp)<n):
            for j in range(len(temp),n):
                lista[i].append(0)
        else:
            continue
    for i in range(n):
        t = 0
        for j in range(N):
            t = t + lista[j][i]
        res.append(t)
    for i in range(len(res)):
        res[i]=res[i]/N

    return res


def M_D_1(arrival_time,max_time,service_time=1/90):
    """
    arrival_time = frequency of the exponential distribution related to the arrival time in 1/seconds
    service_time = deterministic service time in 1/seconds
    max_time = time of simulation in hour to be converted in seconds in the program

    OUTPUT: arrivi e vettore della coda
    """
    #conversion in seconds
    max_seconds = max_time*60*60
    sim_time = 0.0 # simulation time
    t_1 = 0.0 # time for next event (arrival)
    t_2 = max_seconds # time for next event (departure)
    t_n = 0.0 #last event time--> tempo dell'ultimo avvenimento generico
    t_b = 0.0 # last start of busy time--> tempo in cui la queue inizia ad essere non vuota per l'ultima volta
    c = 0 # numero di servizi completati
    queue_aircraft = [] # number of aircraft in the queue
    aircraft = 0
    arrival = [] # time of arrival
    attesa = [] # attesa per gli aerei-->NON SICURO CHE SI CALCOLI COSI'
    # simulation loop
    while(sim_time < max_seconds):
        if(t_1<t_2): #event1:arrival
            sim_time = t_1
            arrival.append(t_1)
            aircraft += 1
            queue_aircraft.append(aircraft)
            t_n = sim_time
            t_1 = sim_time + rm.expovariate(arrival_time)
            if(aircraft==1):
                t_b = sim_time
                t_2 = sim_time + 1/service_time
        else:
            sim_time = t_2
            aircraft = aircraft -1
            queue_aircraft.append(aircraft)
            t_n = sim_time
            attesa.append( t_2 - arrival[c])
            c+=1
            if(aircraft>0):
                t_2=sim_time + 1/service_time
            else:
                t_2 = max_seconds
    return queue_aircraft,arrival,attesa


a,b,c = M_D_1(1/90,24)
a
a = create_distribution(a)
plt.plot(a)

"""
*****************************************************************
***********************SIMULATION PART***************************
*****************************************************************
"""
def simulation_M_D_1(arrival_time,max_time,s_time=1/90,volte =10):
    p = []
    for i in range(volte):
        m_d_1,a,b = M_D_1(arrival_time,max_time,service_time=s_time)
        m_d_1 = create_distribution(m_d_1)
        p.append(m_d_1)

    res = media_vettori(p)
    return res

ciccio = simulation_M_D_1(1/90,24)
plt.plot(ciccio)


def simulation_PSRA(time_freq,freq,fattore_sigma,volte=100):
    """
    questa funzione simula PSRA utilizzando tutte e 4 le distribuzioni che
    abbiamo preso in considerazione (norm,exp,tri,uni)

    INPUT: time_freq = tempo in cui si fa la simulazione in ore
            freq = frequenza del service time
            fattore_sigma = fattore che caratterizza la deviazione standard delle
                            distribuzioni (fattore_sigma/freq)
            volte = numero di volte in cui si vuole far runnare a simulazione
                    (per ogni siulazione)
    dopo aver fatto runnare le simulazioni, per ogni distribuzione si fa la media
    e la si plotta

    OUTPUT: PLOT DELLE DISTRIBUZIONI E VETTORI DELLE DISTRIBUZIONI
    """
    queue_uni_tot = []
    queue_norm_tot = []
    queue_tri_tot = []
    queue_exp_tot = []

    for i in range(volte):
        print(i)
        queue_uni,delay_sim, arr=PSRA(time_freq,"uni",freq,20)
        queue_norm,delay_sim, arr = PSRA(time_freq,"norm",freq,20)
        queue_tri , a,b = PSRA(time_freq,"tri",freq,20)
        queue_exp,c,d = PSRA(time_freq,"exp",freq,20)


        queue_uni = create_distribution(queue_uni)
        queue_norm = create_distribution(queue_norm)
        queue_tri = create_distribution(queue_tri)
        queue_exp = create_distribution(queue_exp)

        queue_uni_tot.append(queue_uni)
        queue_norm_tot.append(queue_norm)
        queue_tri_tot.append(queue_tri)
        queue_exp_tot.append(queue_exp)


    queue_uni_tot = media_vettori(queue_uni_tot)

    queue_norm_tot = media_vettori(queue_norm_tot)

    queue_tri_tot = media_vettori(queue_tri_tot)

    queue_exp_tot = media_vettori(queue_exp_tot)


    uni = list(queue_uni_tot)
    norma = list(queue_norm_tot)
    tri = list(queue_tri_tot)
    esp = list(queue_exp_tot)


    plt.plot(uni,label="UNI")
    plt.plot(norma,label="NORM")
    plt.plot(tri,label="TRI")
    plt.plot(esp,label="EXP")

    plt.legend()
    plt.show()
    plt.savefig("plot/simulation_PSRA.png")


    return uni,norma,tri,esp

freq= 88.88888888888889
m_d_1,r,t = M_D_1(1/freq,24)
m_d_1 = create_distribution(m_d_1)
plt.plot(m_d_1)

a,b,c,d = simulation_PSRA(24,3600/(0.96*41),20,volte = 1000)
plt.figure(1)
plt.subplot(311)
plt.bar(range(len(a)),a,label = "UNI")
plt.legend()
plt.subplot(312)
plt.bar(range(len(b)),b,label = "NORM")
plt.legend()




plt.plot(a,label="UNI")
plt.plot(b,label="NORM")
plt.plot(c,label="TRI")
plt.plot(d,label="EXP")
#plt.plot(ciccio,label="M_D_1")

plt.legend()
plt.show()
plt.savefig("plot/difference_with_M_D_.png")
