import sampling as samp
import numpy as np
import matplotlib.pyplot as plt



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




"costruzione della funzione arrivi"
def arr(N,f="exp",fattore_sigma=20):
    """
    N=numero di slot (derivanti dal lasso temporale indicato)
    f={uni,triang,exp,norm}
    sigma=varianza
    """
    lam=1/90
    delay=np.zeros(N)
    sigma=0


    #caso exp
    if f=="exp":
        delay=np.array(samp.sample_from_exp(lam/fattore_sigma,N))


    if f=="uni":
        max_delay=fattore_sigma*np.sqrt(12)/lam
        delay=np.array(samp.sample_from_uniform(N))
        delay=delay*max_delay


    if f=="norm":
        delay=np.random.normal(0, fattore_sigma/lam, N)
        delay[delay<0]=0



    #calolo arrival
    arrival=np.zeros(N)

    for i in range(N):
        arrival[i]=i/lam + int(delay[i])

    return arrival,delay



"costruzione PSRA"
def PSRA(lasso_temporale_in_ore,distributione,fattore_sigma):

    #conversione in secondi
    T=lasso_temporale_in_ore*60*60
    N=int(T/90)

    #costruzione del vettore degli arrivi con ritardi
    arrival,delay=arr(N,distributione,fattore_sigma)

    #costruzione del PSRA
    queue=np.zeros(N)
    for i in range(1,N):
        arrival_in_slot=len(arrival[(arrival>=90*(i-1)) & (arrival<90*i)])
        queue[i]=queue[i-1]+arrival_in_slot-int(queue[i-1]!=0)

    plt.plot(arrival)
    plt.plot(np.arange(0,T,90))
    plt.show()

    plt.plot(delay/90,label="delay")
    plt.plot(queue,label="queue")
    plt.legend()
    plt.show()
    return queue,delay,arrival


queue,delay,arrival=PSRA(3,"norm",30)
plt.plot(queue)
90*90
8100/60
np.mean
