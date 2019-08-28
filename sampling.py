from scipy.stats import kstest


def sample_from_uniform(N):
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



# exp=lambda x: 2*e**(-2*x)
# prob=exp(linspace(0,2,200))
# cont=sum(prob)
# prob=prob/cont
# s=sample_discrete_rv(prob,10000)
