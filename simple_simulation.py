import sampling as samp
import numpy as np
import matplotlib.pyplot as plt
import pandas
import copy





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










"*********************  our model ********************************"










"costruzione della funzione arrivi"
def arr_m(schedule,capacita,f,fattore_sigma,negative_delays):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """
    lam=1/capacita
    delay=np.zeros(len(schedule))

    #casi distribuzioni
    # if f=="exp":
        # delay=np.array(samp.sample_from_exp(lam/fattore_sigma,len(schedule)))-fattore_sigma/lam

    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        delay=np.random.uniform(-int_a_b,int_a_b,len(schedule))
        if negative_delays==False:

            #delay[delay<0]=0
            delay[delay<0]=abs(delay[delay<0])


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, len(schedule))
        if negative_delays==False:
            #delay[delay<0]=0
            delay[delay<0]=abs(delay[delay<0])

        # if f=="tri":
    # b = (fattore_sigma/lam)*np.sqrt(6)
        # delay = np.random.triangular(0,b/2,b,len(schedule))

    #calolo arrival
    arrival=np.zeros(len(schedule))

    for i in range(len(schedule)):
        arrival[i]=schedule[i] + int(delay[i])

    return arrival,delay





"costruzione PSRA_m"
def PSRA_M(schedule,distributione,capacita,sigma=20, negative_delays=True):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    N=int((schedule[-1]-schedule[0])/capacita)
    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr_m(schedule,capacita,distributione,sigma,negative_delays)

    #costruzione del PSRA
    queue=np.zeros(N)
    #queue_old=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=capacita*(i-1)+schedule[0]) & (arrival<capacita*i+schedule[0])])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)


    return queue,delay,arrival




"****************   simulazioni  *******************************"



def simulation_PSRA_M(N, schedule,capacita,sigma, distrib="norm",negative_delays=True):
    """
    dato N numero di simulazioni
    ritorna un vettore con l'andamento medio delle simul (stady state distr)
    """
    M=int((schedule[-1]-schedule[0])/capacita)
    sim_matrix=np.zeros((N,M))
    sim=np.zeros(M)
    for i in range(N):
        sim_matrix[i],x,y=PSRA_M(schedule,distrib,capacita,sigma,negative_delays)
    for i in range(M):
        sim[i]=np.mean(sim_matrix[:,i])

    return sim,sim_matrix
