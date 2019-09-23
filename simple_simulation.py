import sampling as samp
import numpy as np
import matplotlib.pyplot as plt
import pandas
import copy
import random as rm




"costruzione della funzione arrivi"
def arr(N,f,freq,fattore_sigma,negative_delays):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """
    lam=1/freq
    delay=np.zeros(N)

    #casi distribuzioni
    if f=="exp":

        delay=np.array(np.random.exponential(fattore_sigma/lam, N))-fattore_sigma/lam

    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        delay=np.random.uniform(-int_a_b,int_a_b,N)
        if negative_delays==False:

            delay[delay<0]=0


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, N)
        if negative_delays==False:
            delay[delay<0]=0

    if f=="tri":
        b = (fattore_sigma/lam)*np.sqrt(6)
        delay = np.random.triangular(-b,0,b,N)

    #calolo arrival
    arrival=np.zeros(N)

    for i in range(N):
        arrival[i]=i/lam + int(delay[i])

    return arrival,delay



"costruzione PSRA"
def PSRA(lasso_temporale_in_ore,capacita,distributione,freq,sigma=20, negative_delays=True):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    N=int(T/capacita)

    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr(N,distributione,freq,sigma,negative_delays)


    #costruzione del PSRA
    queue=np.zeros(N)
    #queue_old=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=capacita*(i-1)) & (arrival<capacita*i)])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)


    return queue,delay,arrival




"****************   simulazioni  *******************************"



def simulation_PSRA(N, lasso_temporale,capacita,freq,sigma, distrib="norm"):
    """
    dato N numero di simulazioni
    ritorna un vettore con l'andamento medio delle simul (stady state distr)
    """
    T=(lasso_temporale)*3600
    M=int(T/capacita)
    sim_matrix=np.zeros((N,M))
    sim=np.zeros(M)
    for i in range(N):
        sim_matrix[i],x,y=PSRA(lasso_temporale,capacita,distrib,freq,sigma)
    for i in range(M):
        sim[i]=np.mean(sim_matrix[:,i])

    return sim,sim_matrix


def sim_distribution(sim_matrix):
    n=int(np.max(sim_matrix))+1
    prob=np.zeros(n)
    for i in range(n):
        h=sim_matrix==i
        prob[i]=len(sim_matrix[h])
    prob/=sum(prob)
    return prob


def data_distribution(queue):
    n=int(max(queue))+1
    prob=np.zeros(n)
    for i in range(n):
        h=queue==i
        prob[i]=len(queue[h])
    prob/=sum(prob)
    return prob



"""
############################ M_D_1 ########################################
"""
def M_D_1(arrival_time,max_time):
    """
    arrival_time = frequency of the exponential distribution related to the arrival time in 1/seconds
    = service time
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
                t_2 = sim_time + 1/arrival_time
        else:
            sim_time = t_2
            aircraft = aircraft -1
            queue_aircraft.append(aircraft)
            t_n = sim_time
            attesa.append( t_2 - arrival[c])
            c+=1
            if(aircraft>0):
                t_2=sim_time + 1/arrival_time
            else:
                t_2 = max_seconds
    return queue_aircraft,arrival,attesa

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

def simulation_M_D_1(arrival_time,max_time,volte =10):
    p = []
    for i in range(volte):
        m_d_1,a,b = M_D_1(arrival_time,max_time)
        m_d_1 = create_distribution(m_d_1)
        p.append(m_d_1)

    res = media_vettori(p)
    return res
