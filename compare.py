import math
import numpy as np
import csv
import os

def read(filename):
    acceleration=[]
    angular=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(3)])
            angular.append([float(line[x]) for x in range(3,6)])
    return np.mat(acceleration),np.mat(angular)

def readAcc(filename):
    acceleration=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(3)])
    return np.mat(acceleration)

def compare(m,s):
    filename=os.getcwd() + "\\data\\pca\\result.txt"
    sp=filename.split("\\")
    sp[-2]=m.split("\\")[-2]
    filename="".join(sp)
    m_acc,m_angular=read(m)
    s_acc,s_angular=read(s)
    acc_correlation=[pearson_correlation(m_acc[:,i],s_acc[:,i]) for i in range(3)]
    angular_correlation=[pearson_correlation(m_angular[:,i],s_angular[:,i]) for i in range(3)]
    num=(m.split('-')[-1]).split('.')[0]
    with open(filename,'a') as f:
        f.writelines(num+": \r\n")
        tmp_acc=[str(acc_correlation[i]) for i in range(3) ]
        f.writelines(",".join(tmp_acc)+"\r\n")
        tmp_ang=[str(angular_correlation[i]) for i in range(3)]
        f.writelines(",".join(tmp_ang)+"\r\n")

def compareAcc(m,s):
    filename=os.getcwd() + "\\data\\pca\\result.txt"
    sp=filename.split("\\")
    sp[-2]=m.split("\\")[-2]
    filename="\\".join(sp)
    m_acc=readAcc(m)
    s_acc=readAcc(s)
    acc_correlation=[pearson_correlation(m_acc[:,i],s_acc[:,i]) for i in range(3)]
    num=(m.split('-')[-1]).split('.')[0]
    with open(filename,'a') as f:
        f.writelines(num+": \r\n")
        tmp_acc=[str(acc_correlation[i]) for i in range(3) ]
        f.writelines(",".join(tmp_acc)+"\r\n")

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

def instanceOfCompare():
    filepath = os.getcwd() + "\\data\\pca"
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,13):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            compare(os.path.join(filepath,mfile),os.path.join(filepath,sfile))

if __name__=="__main__":
    filepath = os.getcwd() + "\\data\\RMSD"
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,22):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            compareAcc(os.path.join(filepath,mfile),os.path.join(filepath,sfile))