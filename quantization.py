import numpy as np
import math
import csv
import os
from compare import pearson_correlation,read,readAcc

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
        if bit==preBit and bit!=2:
            counter+=1
        else:
            if counter>=m:
                start=i-counter
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
        flag=True
        if start>=len(bits) or end>=len(bits):
            break
        bit = bits[start]
        for j in range(start,end+1):
            if bit!=bits[j] or bit==2:
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
    mfinal=[m_levelcrossing_bits[i] for i in checked_index]
    sfinal=[s_levelcrossing_bits[i] for i in checked_index]
    error=0.0
    for i in range(len(mfinal)):
        if mfinal[i]!=sfinal[i]:
            error+=1
    return error,mfinal,sfinal


def compareByLevelcrossing(mfile,sfile):

    macc=readAcc(mfile)
    sacc=readAcc(sfile)
    '''
    output.writelines(mfile+" "+sfile+'\r\n')
    output.writelines("acceleration\r\n")'''
    m_key=[]
    s_key=[]
    error=0
    for i in range(3):
        e,mfinal,sfinal=compareData(macc[:,i],sacc[:,i])
        m_key=m_key+mfinal
        s_key=s_key+sfinal
        error+=e
    '''output.writelines("error:"+str(error)+'\r\n')
    output.writelines('len:' + str(len(m_key)) + '\r\n')
    output.writelines(str(m_key)+'\r\n')
    output.writelines(str(s_key)+'\r\n')'''

    return m_key,len(macc),error/len(m_key)


def comparenormal(mfile,sfile):
    m=5
    alpha=0.2
    filepath = os.getcwd() + "\\data\\pca\\normal.txt"
    output=open(filepath,'a',newline="")
    macc,mangular=read(mfile)
    sacc,sangular=read(sfile)
    if pearson_correlation(macc[:50,0],sacc[:50,0])<0:
        macc=-macc
    mbits, mindex = handler(macc[:, 0], m, alpha)
    sbits, sindex = handler(sacc[:, 0], m, alpha)
    common = list(set(mindex).intersection(set(sindex)))
    com_mbits = [mbits[i] for i in common]
    com_sbits = [sbits[i] for i in common]
    counter = 0.0
    for i in range(len(common)):
        if com_mbits[i] != com_sbits[i]:
            counter += 1
    output.writelines(mfile+" "+sfile+'\r\n')
    output.writelines(str(com_mbits)+'\r\n')
    output.writelines(str(com_sbits)+'\r\n')
    output.writelines('error:'+str(counter/len(common))+'\r\n')
    output.writelines('len:'+str(len(common))+'\r\n')

def testlevelcrossing(file):
    filepath=os.getcwd()+"\\data\\"+file
    files=os.listdir(filepath)
    #print(files)
    master="masterlocal"
    slave="slavelocal"

    filepath = os.getcwd() + "\\data\\"+file
    output=open(filepath+"\\levelcrossing.csv",'a',newline="")
    writer=csv.writer(output)

    for i in range(1,45):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            mfilename=os.path.join(filepath,mfile)
            sfilename=os.path.join(filepath,sfile)
            a,b,c=compareByLevelcrossing(mfilename,sfilename)
            writer.writerow([len(a), b, c])


def testnormal():
    filepath=os.getcwd()+"\\data\\pca"
    files=os.listdir(filepath)
    #print(files)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,13):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            mfilename=os.path.join(filepath,mfile)
            sfilename=os.path.join(filepath,sfile)
            comparenormal(mfilename,sfilename)

if __name__=="__main__":
    #testlevelcrossing("RMSD")
    #testlevelcrossing("gyro")
    #testlevelcrossing("AccSpherical")
    #testlevelcrossing("GyroSpherical")
    #testlevelcrossing("AdaptiveAcc")
    #testlevelcrossing("AdaptiveAccSph")
    #testlevelcrossing("AdaptiveGyro")
    #testlevelcrossing("AdaptiveGyroSph")
    testlevelcrossing("leastsquare")
    #testlevelcrossing("leastsquareSph")



