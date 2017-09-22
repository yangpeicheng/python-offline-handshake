import numpy as np
import math
from pca import readData

def getPara(data):
    mean=sum(data)/len(data)
    var=math.sqrt(np.var(data))
    return mean,var

def quantizator(value,q_plus,q_minus):
    if value>q_plus:
        return 1
    elif value<q_minus:
        return 0
    else:
        return 2

def handler(data_list,m,alpha):
    bits=[]
    index=[]
    for i in range(0,len(data_list),m):
        if i+m>len(data_list):
            break
        mean,var=getPara(data_list[i:i+m])
        q_plus=mean+alpha*var
        q_minus=mean-alpha*var
        for j in range(m):
            bit=quantizator(data_list[i+j],q_plus,q_minus)
            bits.append(bit)
            if bit!=2:
                index.append(i+j)
    return bits,index

if __name__=="__main__":
    mdata=np.mat(readData("E:\\SensorData\\pcatest\\masterlocal-9tttransform.csv"))
    mbits,mindex=handler(mdata[:,0],5,0.2)
    sdata=np.mat(readData("E:\\SensorData\\pcatest\\slavelocal-9tttransform.csv"))
    sbits,sindex=handler(sdata[:,0],5,0.2)
    print(len(mindex),len(sindex),len(set(mindex).intersection(set(sindex))))
    common=list(set(mindex).intersection(set(sindex)))
    com_mbits=[mbits[i] for i in common]
    com_sbits=[sbits[i] for i in common]
    counter=0
    for i in range(len(common)):
        if com_mbits[i]!=com_sbits[i]:
            counter+=1
    print(counter)
