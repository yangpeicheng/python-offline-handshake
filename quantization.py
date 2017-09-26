import numpy as np
import math
import csv

def read(filename):
    acc=[]
    angular=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acc.append([float(line[x]) for x in range(3)])
            angular.append([float(line[x]) for x in range(3,6)])
    return np.mat(acc),np.mat(angular)

def getPara(data):
    mean=sum(data)/len(data)
    var=math.sqrt(np.var(data))
    return mean,var

def quantizer(value,q_plus,q_minus):
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
            bit=quantizer(data_list[i+j],q_plus,q_minus)
            bits.append(bit)
            if bit!=2:
                index.append(i+j)
    return bits,index

def levelcrossing(data_list,m,alpha):
    bits=[]
    index=[]
    mean,var=getPara(data_list)
    q_plus = mean + alpha * var
    q_minus = mean - alpha * var
    i=1
    counter=1
    preBit=quantizer(data_list[0],q_plus,q_minus)
    while i<len(data_list):
        bit=quantizer(data_list[i],q_plus,q_minus)
        bits.append(bit)
        if bit==preBit:
            counter+=1
        else:
            if counter>=m:
                start=i-m
                end=i-1
                index.append(int((start+end)/2))
            counter=1
            preBit=bit
        i+=1
    return bits,index

def check_levelcrossing(bits,index,m):
    checked_index=[]
    for i in index:
        start=i-math.floor((m-2)/2)
        end=i+math.ceil((m-2)/2)
        bit=bits[start]
        flag=True
        if end>=len(bits):
            break
        for j in range(start,end+1):
            if bit!=bits[j]:
                flag=False
                break
        if flag:
            checked_index.append(i)
    return checked_index

def compareData(mdata,sdata):
    m=5
    alpha=0.2
    m_levelcrossing_bits,m_levelcrossing_index=levelcrossing(mdata,m, alpha)
    s_levelcrossing_bits,s_levelcrossing_index = levelcrossing(sdata, m, alpha)
    checked_index = check_levelcrossing(s_levelcrossing_bits, m_levelcrossing_index, m)
    print(checked_index)
    mfinal=[m_levelcrossing_bits[i] for i in checked_index]
    sfinal=[s_levelcrossing_bits[i] for i in checked_index]
    error=0
    for i in range(len(mfinal)):
        error+=1
    return error,mfinal,sfinal


def compareByLevelcrossing(mfile,sfile):
    output=open("E:\SensorData\pca\levelcrossing.txt",'a',newline="")
    macc,mangular=read(mfile)
    sacc,sangular=read(sfile)
    output.writelines(mfile+" "+sfile)
    output.writelines("acceleration")
    for i in range(3):
        error,mfinal,sfinal=compareData(macc[:,i],sacc[:,i])
        output.writelines("error:"+str(error))
        output.writelines(str(mfinal))
        output.writelines(str(sfinal))
    output.writelines("angular")
    for i in range(3):
        error,mfinal,sfinal=compareData(mangular[:,i],sangular[:,i])
        output.writelines("error:"+str(error))
        output.writelines(str(mfinal))
        output.writelines(str(sfinal))


if __name__=="__main__":
    '''   m=5
       alpha=0.2
       mdata=np.mat(readData("E:\\SensorData\\pcatest\\masterlocal-9tttransform.csv"))
       sdata=np.mat(readData("E:\\SensorData\\pcatest\\slavelocal-9tttransform.csv"))
       mbits, mindex = handler(mdata[:, 0], m, alpha)
       sbits,sindex=handler(sdata[:,0],m,alpha)
       common=list(set(mindex).intersection(set(sindex)))
       com_mbits=[mbits[i] for i in common]
       com_sbits=[sbits[i] for i in common]
       counter=0
       for i in range(len(common)):
           if com_mbits[i]!=com_sbits[i]:
               counter+=1
       print(counter)

       m_levelcrossing_bits,m_levelcrossing_index=levelcrossing(mdata[:,1],m, alpha)
       s_levelcrossing_bits,s_levelcrossing_index = levelcrossing(sdata[:, 1], m, alpha)
       checked_index=check_levelcrossing(s_levelcrossing_bits,m_levelcrossing_index,m)
       print(m_levelcrossing_index)
       print(s_levelcrossing_index)
       print(checked_index)
       print([m_levelcrossing_bits[i] for i in checked_index])
       print([s_levelcrossing_bits[i] for i in checked_index])'''
    compareByLevelcrossing("E:\SensorData\pca\masterlocal-1.csv","E:\SensorData\pca\slavelocal-1.csv")

