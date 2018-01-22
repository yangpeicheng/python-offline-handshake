import math
import csv
import numpy as np

def pearson_correlation(x,y):
    mean_x=sum(x)/len(x)
    mean_y=sum(y)/len(y)
    lxx=0
    lyy=0
    lxy=0
    for i in range(min(len(x),len(y))):
        lxy+=(x[i]-mean_x)*(y[i]-mean_y)
        lxx+=(x[i]-mean_x)*(x[i]-mean_x)
        lyy+=(y[i]-mean_y)*(y[i]-mean_y)
    return float(lxy/math.sqrt(lxx*lyy))

def align(mfile,sfile):
    m,mt=readAccelerationMatrix(mfile)
    s,st=readAccelerationMatrix(sfile)
    length = 50
    m_magnitude=[getMagnitude(m[i]) for i in range(length*2)]
    s_magnitude=[getMagnitude(s[i]) for i in range(length*2)]
    m_start=0
    s_start=0
    correlation=0
    for i in range(length):
        for j in range(length):
            tmp=pearson_correlation(m_magnitude[i:i+length],s_magnitude[j:j+length])
            if tmp>correlation:
                m_start=i
                s_start=j
                correlation=tmp
    return m_start,s_start

def getMagnitude(data):
    sum=0
    for i in data:
        sum+=i*i
    return math.sqrt(sum)

def readAll(filename):
    data=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            data.append([float(line[x]) for x in range(len(line))])
    return data

def readAcc(filename):
    acceleration=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(0,3)])
    return acceleration

def readAccelerationMatrix(filename):
    acceleration=[]
    matrix=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(0,3)])
            matrix.append(np.mat([float(line[x]) for x in range(3,12)]).reshape(3,3))
    return acceleration,matrix

def readGravity(filename):
    gravity=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            gravity.append([float(line[x]) for x in range(6,9)])
    return gravity

def readAccGyro(filename):
    acceleration=[]
    gyro=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(0,3)])
            gyro.append([float(line[x]) for x in range(12,15)])
    return acceleration,gyro

def readAccMatGyro(filename):
    acceleration=[]
    matrix=[]
    gyro=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(0,3)])
            matrix.append(np.mat([float(line[x]) for x in range(3,12)]).reshape(3,3))
            gyro.append([float(line[x]) for x in range(12,15)])
    return acceleration,matrix,gyro

def shift_central(m):
    s=[0 for i in range(3)]
    for i in range(len(m)):
        for j in range(3):
            s[j]+=m[i][j]
    mean=[s[j]/len(m) for j in range(3)]
    for i in range(len(m)):
        for j in range(3):
            m[i][j]-=mean[j]
    return m