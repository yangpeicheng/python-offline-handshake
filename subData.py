import csv
import math
import numpy as np
def extract(m,start,end):
    new = m.split('.')[0] + "t.csv"
    output=open(new,'w',newline="")
    write=csv.writer(output)
    with open(m) as f:
        reader=csv.reader(f)
        index=0
        for line in reader:
            index+=1
            if index>start and index<end:
                write.writerow(line)

def init(data):
    window=[]
    window_size=5
    magnitude=[]
    variance=[]
    for i in data:
        mag=getMagnitude(i)
        window.append(mag)
        if len(window)==window_size:
            magnitude.append(mag)
            variance.append(np.var(window))
            window.remove(0)
    return magnitude,variance

def getMagnitude(data):
    sum=0
    for i in data:
        sum+=i*i
    return math.sqrt(sum)

#data ---acceleration data
def findHandShake(data):
    magnitude,variance=init(data)
    MAGNITUDE_THRESHOLD = 1.0
    VARIANCE_THRESHOLD = 0.2
    preState=True
    downIndex=[]
    upIndex=[]
    for i in range(len(magnitude)):
        currentState=(variance[i]<VARIANCE_THRESHOLD) and (magnitude[i]<MAGNITUDE_THRESHOLD)
        if preState==True and currentState==False:
            downIndex.append(i)
        elif preState==False and currentState==True:
            upIndex.append(i)
        preState=currentState
    i=0
    while i<min(len(upIndex),len(downIndex)-1):
        if downIndex[i+1]-upIndex[i]<5:
            downIndex.remove(i+1)
            upIndex.remove(i)
        else:
            i+=1
    start=downIndex[0]
    end=upIndex[0]
    length=end-start
    for j in range(1,min(len(upIndex),len(downIndex))):
        if upIndex[j]-downIndex[j]>length:
            length=upIndex[j]-downIndex[j]
            end=upIndex[j]
            start=downIndex[j]
    return start,end

def readCompleteData(filename):
    acceleration=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(3,6)])
    return acceleration




if __name__=="__main__":
    extract("E:\\SensorData\\pcatest\\masterlocal-9.csv")
    extract("E:\\SensorData\\pcatest\\slavelocal-9.csv")


