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
    left = 0.4/lam
    right = 1.6/lam
    service_dix = np.random.triangular(left,mode,right,N-1)/90
    print(service_dix)
    for i in range(1,N):
        # numero di aerei che arrivano nella slot considerata
        arrival_in_slot = len(arrival[(arrival>=90*(i-1)) & (arrival<90*i)])
        if(queue[i-1]!=0):
            queue[i] = queue[i-1]+arrival_in_slot - int(service_dix[i-1])
        else:
            queue[i] = queue[i-1]+arrival_in_slot
    return queue,delay,arrival

queue_u,delay_u,arrival_u=PSRA_G(3,"uni",20)
queue,delay,arrival=sm.PSRA(3,"uni",20)
plt.plot(queue_u,label="triangular service")
plt.plot(queue,label="deterministic service")
plt.legend()
