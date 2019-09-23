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
        delay=np.array(samp.sample_from_exp(lam/fattore_sigma,N))-fattore_sigma/lam

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
        delay = np.random.triangular(0,b/2,b,N)

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

def M_D_1(arrival_time,max_time):

    arrival_time = frequency of the exponential distribution related to the arrival time in 1/seconds
    = service time
    max_time = time of simulation in hour to be converted in seconds in the program

    OUTPUT: arrivi e vettore della coda
    
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


def simulation_M_D_1(iterazioni,service_time,max_time):
    list_simulation = []
    for i in range(iterazioni):
        queue_aircraft,arrival,attesa = M_D_1(service_time,max_time)
        list_simulation.append(queue_aircraft)
    return list_simulation


a = simulation_M_D_1(100,1/90,24)

def create_dix_M_D_1(lista):
    maximo = trova_massimo(lista)
    print(maximo)
    # trasformo le liste tutte della stessa lunghezza con un ciclo for
    for i in range(len(lista)):
        if len(lista[i])<maximo:
            for j in range(0,maximo - len(lista)-1):
                lista[i].append(0)
    return lista



def trova_massimo(lista):
    res = 0
    for i in range(len(lista)):
        if len(lista[i])>res:
            res = len(lista[i])
    return res

ll = [[1,2,3,4],[1,2,3],[1,1,1,1,1,1],[1,2,3,4,5,6,7,8]]
r = trova_massimo(ll)
r
q = create_dix_M_D_1(ll)

q
"""
