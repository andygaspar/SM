import sampling as samp
import numpy as np
import matplotlib.pyplot as plt
import pandas
import copy



"""
# TODO:

- leggere articoli presenti nel paper, in particolare nell'ordine: Iovanella, Willemain, Guadagni (sulla stationary distribution), possibilmentte gli altri

- tramite gli articoli capire bene se siamo sulla strada giiusta specialmente per quello che riguarda l'interpretazione e quindi l'implementazione della distribuzione dei ritardi (con particolare riguardo ai valori di sigma e lamda)

- ALBI scrivere agli altri professori del paper

- GASPA scrivere a castelli

- cercare autonomamente dataset

obiettivi nell'ordine:
1)confermare i risultati del paper
2)implementare e confermare la stationary distribution
3)varie ed eventuali idee di modifiche
4)se a disposizione il dataset originale fare un ragionamento sul flusso OCK escluso dal paper


"""






"""

def tot_dist(a,b):

    return sum(np.abs(a-b))/len(a)

def hell_dist(a,b):
    return np.sqrt(sum((np.abs(np.sqrt(a)-np.sqrt(b)))**2))/np.sqrt(2)
plt.plot(np.random.choice(delay_sim,len(clean)),label="delay_sim")
plt.plot(delay,label="clean")
plt.legend()
plt.show()


a=np.array([1,2,3,1,2,3,1])
b=np.array([1,2,3,1,1,3,1])
tot_dist(a,b)
# arrival=np.zeros(100)
# lam=1/90
# delay=np.array(samp.sample_from_exp(np.sqrt(lam/20),100))
# for i in range(100):




# print(arrival)
# print(delay)
# min_delay=delay/60
# min_delay
#

#
# plt.plot(min_delay)
# plt.plot(arrival)
# plt.plot(delay)

"""


"costruzione della funzione arrivi"
def arr(N,f,freq,fattore_sigma=20):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """
    lam=1/freq
    delay=np.zeros(N)



    #caso exp
    if f=="exp":
        delay=np.array(samp.sample_from_exp(fattore_sigma/lam,N))


    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        delay=np.random.uniform(-int_a_b,int_a_b,N)
        delay[delay<0]=0


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, N)
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
def PSRA(lasso_temporale_in_ore,distributione,freq,fattore_sigma):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    N=int(T/freq)

    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr(N,distributione,freq,fattore_sigma)


    #costruzione del PSRA
    queue=np.zeros(N)
    #queue_old=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=freq*(i-1)) & (arrival<freq*i)])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)



    return queue,delay,arrival







"***************************************************"
"costruzione della funzione arrivi"
def arr_2(N,f,freq,fattore_sigma=20):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """
    lam=1/freq
    delay=np.zeros(N)



    #caso exp
    if f=="exp":
        delay=np.array(samp.sample_from_exp(fattore_sigma/lam,N))


    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        int_a_b=fattore_sigma/2*np.sqrt(12)/lam
        delay=np.random.uniform(-int_a_b,int_a_b,N)


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, N)

    if f=="tri":
        b = (20/lam)*np.sqrt(6)
        delay = np.random.triangular(0,b/2,b,N)




    #calolo arrival
    arrival=np.zeros(N)

    for i in range(N):
        arrival[i]=i/lam + int(delay[i])

    return arrival,delay




"costruzione PSRA"
def PSRA_2(lasso_temporale_in_ore,distributione,freq,fattore_sigma):
    """
    dato lasso temporale, distribuzione: ("exp", "uni", "norm", "tri"), lam, fattore_sigma
    ritorna liste con queue, delay, arrival
    """

    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    N=int(T/freq)

    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr_2(N,distributione,freq,fattore_sigma)


    #costruzione del PSRA
    queue=np.zeros(N)
    #queue_old=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=freq*(i-1)) & (arrival<freq*i)])
        #queue_old[i]=queue_old[i-1]+arrival_in_slot-int(queue_old[i-1]!=0)
        queue[i]=queue[i-1]   +   arrival_in_slot   -    int(queue[i-1]!=0)



    return queue,delay,arrival






"""
"simulazioni"

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
