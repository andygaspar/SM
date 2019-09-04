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


lam = 1/90
a,b,c = M_D_1(1/90,1)
a

for i in range(len(c)):
    c[i]=c[i]/90

c

def create_distribution(v):
    "funzione che crea una distribuzione discreta di probabilità"
    "serve per avere la distribuzione sulle possibili lunghezze della queue"
    v = np.array(v)
    N = len(v)
    massimo = int(max(v))
    dix = np.zeros(massimo + 1)
    # viaggio su tutte le possibili lunghezze della coda
    for i in range(massimo+1):
        cont = len(v[(v==i)])
        dix[i] = cont/N
    return dix


md_dix =create_distribution(a)

queue_u,delay_u,arrival_u=PSRA_G(3,"uni",20)
queue,delay,arrival=sm.PSRA(3,"uni",20)
plt.plot(queue_u,label="triangular service")
plt.plot(queue,label="deterministic service")
plt.plot(a, label="M/D/1")
plt.legend()
plt.grid()



domain = []
for i in range(12):
    domain.append(i)
x = create_distribution(queue_u)
y = create_distribution(a)


plt.plot(x,label = "PRSA",)
plt.plot(y,label = "M/D/1")
plt.grid()
plt.legend()
