from scipy.stats import kstest
import time
import numpy


def sample_from_uniform(N):
    """
    costruisce un vettore random in [0,1]
    """
    a=5
    c=3
    m=2**10
    t=time.time()
    t=int((t%1)*10**16)
    rand_seq=[t%m]
    for i in range(N-1):
        rand_seq.append((a*rand_seq[i]+c)%m)
        rand_seq[i]=rand_seq[i]/m
    rand_seq[N-1]=rand_seq[N-1]/m
    return rand_seq



def sample_from_exp(lam,N):
    U=sample_from_uniform(N)
    rand_seq=[]
    for i in range(N):
        rand_seq.append(-(numpy.log(1-U[i]))/lam)
    return rand_seq



def sample_discrete_rv(P,N):
    index=list(P.argsort())
    index.reverse()
    P=sorted(P)
    P.reverse()
    S=sample_from_uniform(N)
    sample=zeros(N)
    cum=[P[0]]
    for i in range(1,len(P)):
        cum.append(cum[i-1]+P[i])
    for i in range(len(S)):
        for j in range(len(cum)):
            if S[i]<cum[j]:
                sample[i]=index[j]
                break

    return sample



def rejection_sampling(f,N,a,b):
    """g is uniform; to obtain g>=f we compute the max M; c is obtained such that int(M) in [a,b] is equal to 1"""

    I=linspace(a,b,10**5)
    M=max(f(I))
    g= lambda x:M
    c=1/(M*(b-a))
    u=sample_from_uniform(N)
    u_y=sample_from_uniform(N)

    sample=zeros(N)
    reject=0
    i=0
    j=0
    NN=N
    while(j<N):
        y=(u_y)[i]/c
        if u[i]<=f(y)/g(y):
            sample[j]=y
            j+=1
        else:
            reject+=1;
        i+=1
        if(i==NN and reject>0):
            u=sample_from_uniform(reject)
            u_y=sample_from_uniform(reject)
            i=0
            NN=reject

    print(reject)

    return sample

# exp=lambda x: 2*e**(-2*x)
# prob=exp(linspace(0,2,200))
# cont=sum(prob)
# prob=prob/cont
# s=sample_discrete_rv(prob,10000)
