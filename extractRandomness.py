import math
from quantization import compareByLevelcrossing
from statsmodels.tsa.stattools import pacf
from matplotlib import pyplot as plt
import os
import csv
CODING_LEN = 4
MALKOV_ORDER = 4

def loadCodeTable(CODING_LEN):
    code=[[] for i in range(2<<(CODING_LEN-1))]
    tmp=[[] for i in range(CODING_LEN+1)]
    for i in range(CODING_LEN+1):
        count=combination(CODING_LEN,i)
        for j in range(count):
            tmp[i].append(j)
    for i in range(len(code)):
        c=numOfOne(i)
        codelen=math.ceil(math.log2(combination(CODING_LEN,c)))
        if codelen==0:
            codelen=1
        k=tmp[c].pop(0)
        key=num2bit(k,codelen)
        code[i]=key
    '''for i in range(len(code)):
        print(num2bit(i,CODING_LEN),code[i])'''
    return code

def num2bit(n,l):
    bit=[]
    while n>0:
        t=n%2
        bit.insert(0,t)
        n=int(n/2)
    while len(bit)<l:
        bit.insert(0,0)
    return bit

def numOfOne(n):
    count=0
    while n>0:
        t=n%2
        n=int(n/2)
        if t==1:
            count+=1
    return count

def combination(a,b):
    up=1
    low=1
    for i in range(b):
        up*=(a-i)
    for i in range(2,b+1):
        low*=i;
    return int(up/low)



def subStringByMalkov(bits,malkov_order):
    stringNum=2<<(malkov_order-1)
    subStrings=[[] for i in range(stringNum)]
    for i in range(len(bits)):
        if i+malkov_order>=len(bits):
            break
        strIndex = 0
        for j in range(malkov_order):
            strIndex=strIndex*2+bits[i+j]
        subStrings[strIndex].append(bits[i+malkov_order])
    return subStrings

def bit2num(bits):
    val=0
    for i in range(len(bits)):
        val=val*2+bits[i]
    return val

def codeByTable(subStrings,CODING_LEN,codingTable):
    key=[]
    for subString in subStrings:
        stringLen=len(subString)
        if stringLen>0:
            for i in range(0,stringLen,CODING_LEN):
                if i+CODING_LEN>stringLen:
                    temp=subString[i:stringLen]
                    b=0
                    for j in range(0,i+CODING_LEN-stringLen):
                        temp.append(b)
                        b=1-b
                else:
                    temp=subString[i:i+CODING_LEN]
                key.extend(codingTable[bit2num(temp)])
    return key

def extractRandomness(bits,malkov_order,CODING_LEN):
    subStrings=subStringByMalkov(bits,malkov_order)
    table=loadCodeTable(CODING_LEN)
    return codeByTable(subStrings,CODING_LEN,table)

def plotPacf(data):
    lag_pacf=pacf(data,nlags=10)
    print(lag_pacf)
    plt.bar(range(1,12),lag_pacf)
    plt.show()

def batch(file):
    filepath=os.getcwd()+"\\data\\"+file
    files=os.listdir(filepath)
    #print(files)
    master="masterlocal"
    slave="slavelocal"

    filepath = os.getcwd() + "\\data\\"+file
    output=open(filepath+"\\extractRandom.csv",'a',newline="")
    writer=csv.writer(output)

    for i in range(1,45):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            mfilename=os.path.join(filepath,mfile)
            sfilename=os.path.join(filepath,sfile)
            a,b,c=compareByLevelcrossing(mfilename,sfilename)
            key=extractRandomness(a,4,4)
            writer.writerow([len(key),len(key)/b,len(a)/len(key)])

if __name__=="__main__":


   ''' num=str(40)
    mfile="C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAcc\\masterlocal-"+num+".csv"
    sfile="C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAcc\\slavelocal-"+num+".csv"
    key, b, c = compareByLevelcrossing(mfile, sfile)
    finalkey=extractRandomness(key,4,4)
    print(len(finalkey),finalkey)
    mfile="C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAccSph\\masterlocal-"+num+".csv"
    sfile="C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAccSph\\slavelocal-"+num+".csv"
    key, b, c = compareByLevelcrossing(mfile, sfile)
    finalkey=extractRandomness(key,4,4)
    print(len(finalkey),finalkey)'''
   batch("AdaptiveAcc")
   batch("AdaptiveAccSph")