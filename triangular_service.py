import numpy as np
import simple_simulation as sm
import matplotlib.pyplot as plt
import queue
import random as rm


"Nel lavoro precedente abbiamo considerato di servire sempre un aereo per slot"
"cioè un aereo ogni 90 secondi--->service time is constant"


def PSRA_G(lasso_temporale_in_ore,distribuzione,fattore_sigma):
    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    # numero di slot che considero
    N=int(T/90)
    #abbiamo gli arrivi e i ritardi
    arrival,delay = sm.arr(N,distribuzione,fattore_sigma)
    #creazione del vettore contenente la queue
    queue = np.zeros(N)
    lam = 1/90
    mode = 0.8/lam
    left = 0.3/lam
    right = 1.5/lam
    service_dix = np.random.triangular(left,mode,right,N-1)/90
    #print(service_dix)
    for i in range(1,N):
        # numero di aerei che arrivano nella slot considerata
        arrival_in_slot = len(arrival[(arrival>=90*(i-1)) & (arrival<90*i)])
        if(queue[i-1]!=0):
            queue[i] = queue[i-1]+arrival_in_slot - round(service_dix[i-1])
        else:
            queue[i] = queue[i-1]+arrival_in_slot
    return queue,delay,arrival


# questa simulazione invece il service time è deterministico, però gli arrivi
# non seguono più il PSRA ma sono arrivi che si basano su Poisson dix

def M_D_1(lam,mu,max_time):
    "lam = mean of arrival of airctraft (poisson dix)"
    " mu = frequency of service time (deterministic)"
    " max_time = considered time_lapse"
    T = max_time*60*60
    N=int(T*mu)
    arrival_poisson = rm.expovariate(lam)
    arrival = np.zeros(N)
    arrival[0] = arrival_poisson
    for i in range(1,N):
        arrival_poisson = rm.expovariate(lam)
        arrival[i] = arrival[i-1] + arrival_poisson
    queue = np.zeros(N)
    for i in range(1,N):
        arrival_in_slot = len(arrival[(arrival>=90*(i-1)) & (arrival<90*i)])
        if i>1:
            queue[i]=queue[i-1]+arrival_in_slot-int(queue[i-1]!=0)
        else:
            queue[i]=queue[i-1]+arrival_in_slot-1


    return queue,arrival

lam = 1/90
a,b = M_D_1(1/83,1/90,3)
max(a)
def create_distribution(v):
    "funzione che crea una distribuzione discreta di probabilità"
    "serve per avere la distribuzione sulle possibili lunghezze della queue"
    N = len(v)
    massimo = int(max(v))
    dix = np.zeros(massimo + 1)
    # viaggio su tutte le possibili lunghezze della coda
    for i in range(massimo+1):
        cont = len(v[(v==i)])
        dix[i] = cont/N
    return dix




queue_u,delay_u,arrival_u=PSRA_G(3,"uni",20)
queue,delay,arrival=sm.PSRA(3,"uni",20)
plt.plot(queue_u,label="triangular service")
plt.plot(queue,label="deterministic service")
plt.legend()



domain = []
for i in range(12):
    domain.append(i)
x = create_distribution(queue_u)
y = create_distribution(a)
plt.plot(x,label = "PRSA")
plt.plot(y,label = "M/D/1")
plt.legend()
