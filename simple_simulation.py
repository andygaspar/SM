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
        delay=np.array(samp.sample_from_exp(fattore_sigma/lam,N))

    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        if negative_delays==False:
            delay=np.random.uniform(-int_a_b,int_a_b,N)
            delay[delay<0]=0


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, N)
        if negative_delays==False:
            delay[delay<0]=0

    if f=="tri":
        b = (20/lam)*np.sqrt(6)
        delay = np.random.triangular(0,b/2,b,N)

    #calolo arrival
    arrival=np.zeros(N)

    for i in range(N):
        arrival[i]=i/lam + int(delay[i])

    return arrival,delay



"costruzione PSRA"
def PSRA(lasso_temporale_in_ore,distributione,freq,sigma=20, negative_delays=True):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    N=int(T/freq)

    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr(N,distributione,freq,sigma,negative_delays)

    #costruzione del PSRA
    queue=np.zeros(N)

    #queue_old=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=freq*(i-1)) & (arrival<freq*i)])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)


    return queue,delay,arrival




"****************   simulazioni  *******************************"



def simulation_PRSA(N, start_time, end_time,freq,sigma, distrib="norm"):
    """
    dato N numero di simulazioni
    ritorna un vettore con l'andamento medio delle simul (stady state distr)
    """
    T=(end_time-start_time)*3600
    M=int(T/freq)
    sim_matrix=np.zeros((N,M))
    sim=np.zeros(M)
    for i in range(N):
        sim_matrix[i],x,y=PSRA(end_time-start_time,distrib,freq,sigma)
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
sim,sim_matrix=simulation_PRSA(1000, 3, 10,90,20)
plt.plot(prob)
"""







"""
"simulazioni"
""
k=20
dist=np.zeros(2000)
for i in range(2000):

    queue_u,delay_u,arrival_u=PSRA(3,"uni",k)
    queue_n,delay_n,arrival_n=PSRA(3,"norm",k)
    dist[i]=tot_dist(queue_u,queue_n)

np.mean(dist)
plt.plot(dist)
plt.plot(queue_u,label="uniform")
plt.plot(queue_n,label="normal")
plt.legend()



queue_u,delay_u,arrival_u=PSRA(3,"uni",30,200)
queue_u_1,delay_u_1,arrival_u_1=PSRA_(3,"uni",k)
plt.plot(queue_u,label="uniform")
10
queue_u==queue_u_1

queue_n,delay_n,arrival_n=PSRA(3,"norm",k)
queue_tri,delay_tri,arrival_tri=PSRA(3,"tri",k)
d=tot_dist(queue_u,queue_n)
plt.plot(queue_u,label="uniform")
plt.plot(queue_n,label="normal")
plt.plot(queue_tri,label="triangular")
plt.legend()
plt.title(d)
"""
