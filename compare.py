import math
import numpy as np
import csv


def read(filename):
    acceleration=[]
    angular=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([line[x] for x in range(3)])
            angular.append([line[x] for x in range(3,6)])
    return np.mat(acceleration),np.mat(angular)

def compare(m,s):
    m_acc,m_angular=read(m)
    s_acc,s_angular=read(s)


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
    return lxy/math.sqrt(lxx*lyy)

