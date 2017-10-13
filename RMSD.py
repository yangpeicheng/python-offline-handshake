import numpy as np
import os
import csv
from Utils import readAccelerationMatrix,align,shift_central
from matplotlib import pyplot as plt


def qmul(p,q):
    a0=p[0]
    b0=q[0]
    a=np.array(p[1:4])
    b=np.array(q[1:4])
    acb=a0*b+b0*a+np.cross(a,b)
    pq=[a0*b0-np.dot(a,b)]+acb.tolist()
    return pq

def rotquat(p,u):
    p=[0]+p
    uc=[u[0],-u[1],-u[2],-u[3]]
    up=qmul(u,p)
    upuc=qmul(up,uc)
    return upuc

def residuum(X,Y):
    R=np.dot(X,Y.transpose()).tolist()
    F=np.array([[R[0][0]+R[1][1]+R[2][2],R[1][2]-R[2][1],R[2][0]-R[0][2],R[0][1]-R[1][0]],
       [R[1][2]-R[2][1],R[0][0]-R[1][1]-R[2][2],R[0][1]+R[1][0],R[0][2]+R[2][0]],
       [R[2][0]-R[0][2],R[0][1]+R[1][0],-R[0][0]+R[1][1]-R[2][2],R[1][2]+R[2][1]],
       [R[0][1]-R[1][0],R[0][2]+R[2][0],R[1][2]+R[2][1],-R[0][0]-R[1][1]+R[2][2]]
       ])
    V,D=np.linalg.eig(F)
    ev=V[0]
    evv=D[:,0]
    maxval=ev
    minval=ev
    maxindex=0
    minindex=0
    for i in range(1,4):
        if V[i]>maxval:
            maxval=V[i]
            maxindex=i
        elif V[i]<minval:
            minval=V[i]
            minindex=i
    evv=D[:,maxindex]
    evv=evv.tolist()
    return evv

def reser(X,u):
    result=[]
    n,m=X.shape
    for i in range(m):
        tmp=X[:,i].transpose().tolist()[0]
        result.append(rotquat(tmp,u)[1:4])
    return result

def output(file,data):
    str=file.split('\\')
    str[-2]="RMSD"
    outputfile="\\".join(str)
    with open(outputfile,'w',newline="") as f:
        out=csv.writer(f)
        for i in data:
            out.writerow(i)

def main_test():
    filepath = os.getcwd()+"\\data\\transform"
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,22):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            m=os.path.join(filepath,mfile)
            s=os.path.join(filepath,sfile)
            m_a,m_matrix=readAccelerationMatrix(m)
            s_a, s_matrix = readAccelerationMatrix(s)
            m_a=shift_central(m_a)
            s_a=shift_central(s_a)
            m_start,s_start=align(m,s)
            m_a=m_a[m_start:]
            s_a=s_a[s_start:]
            if len(m_a)>len(s_a):
                l=len(s_a)
            else:
                l = len(m_a)
            m_a = np.mat(m_a[:l]).transpose()
            s_a=np.mat(s_a[:l]).transpose()
            testnum=int(l/4)
            tm_a =m_a[:,:testnum]
            ts_a=s_a[:,:testnum]
            evv=residuum(tm_a,ts_a)
            data=reser(m_a,evv)
            output(m,data)
            output(s,s_a.transpose().tolist())

if __name__=="__main__":
    m=os.getcwd()+"\\data\\transform"+"\\masterlocal-20.csv"
    s=os.getcwd()+"\\data\\transform"+"\\slavelocal-20.csv"
    m_a, m_matrix = readAccelerationMatrix(m)
    s_a, s_matrix = readAccelerationMatrix(s)
    m_a = shift_central(m_a)
    s_a = shift_central(s_a)
    m_start, s_start = align(m, s)
    m_a = m_a[m_start:]
    s_a = s_a[s_start:]
    if len(m_a) > len(s_a):
        l = len(s_a)
    else:
        l = len(m_a)
    m_a = np.mat(m_a[:l]).transpose()


    row,col=m_a.shape
    var_length=50
    variances=[[] for i in range(3)]
    for i in range(0,col-var_length):
        tmp=[float(np.var(m_a[j,i:i+var_length])) for j in range(3)]
        for j in range(3):
            variances[j].append(tmp[j])
    x=range(col)
    print(variances)
    plt.plot(variances[0],color='red')
    plt.plot(variances[1],color='blue')
    plt.plot(variances[2],color='green')
    plt.show()


    s_a = np.mat(s_a[:l]).transpose()
    testnum = int(l / 4/3)
    index=[0,105,248]
    data=[]
    tm_a = m_a[:, index[0]:index[0]+testnum]
    ts_a = s_a[:, index[0]:index[0]+testnum]
    evv=residuum(tm_a,ts_a)
    data+=reser(m_a[:,:index[1]],evv)
    tm_a = m_a[:, index[1]:index[1]+testnum]
    ts_a = s_a[:, index[1]:index[1]+testnum]
    evv=residuum(tm_a,ts_a)
    data += reser(m_a[:, index[1]:index[2]], evv)
    tm_a = m_a[:, index[2]:index[2]+testnum]
    ts_a = s_a[:, index[2]:index[2]+testnum]
    evv=residuum(tm_a,ts_a)
    data += reser(m_a[:, index[2]:], evv)
    output(m, data)
    output(s, s_a.transpose().tolist())