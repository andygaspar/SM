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




def simulation_PSRA(time_req,freq,fattore_sigma,volte=100):
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
        queue_uni,delay_sim, arr=PSRA(24,"uni",freq,20)
        queue_norm,delay_sim, arr = PSRA(24,"norm",freq,20)
        queue_tri , a,b = PSRA(24,"tri",freq,20)
        queue_exp,c,d = PSRA(24,"exp",freq,20)

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




a,b,c,d = simulation_PSRA(24,90,20,volte = 1000)
