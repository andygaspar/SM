import numpy as np
import simple_simulation as sm
import matplotlib.pyplot as plt


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
# vengono fatti con mean = 20/lam e 30/lam
#NON SICURO DI QUESTO---> RIVEDERE
def M_D_1(lasso_temporale_in_ore,fattore_sigma):
    lam = 1/90
    T = lasso_temporale_in_ore*60*60
    N=int(T/90)
    arrival_poisson = np.random.poisson(fattore_sigma/lam,N)
    arrival = np.zeros(N)
    for i in range(N):
        arrival[i] = i/lam + int(arrival_poisson[i])
    queue = np.zeros(N)
    for i in range(1,N):
        arrival_in_slot = len(arrival[(arrival>=90*(i-1)) & (arrival<90*i)])
        queue[i]=queue[i-1]+arrival_in_slot-int(queue[i-1]!=0)
    return queue


a = M_D_1(3,20)

plt.plot(a)



#queue_u,delay_u,arrival_u=PSRA_G(3,"uni",20)
#queue,delay,arrival=sm.PSRA(3,"uni",20)
#plt.plot(queue_u,label="triangular service")
#plt.plot(queue,label="deterministic service")
#plt.legend()
