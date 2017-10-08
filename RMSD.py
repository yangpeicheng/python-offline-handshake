import numpy as np
import os
import csv
from pca import readAccelerationMatrix

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
    print(R)
    F=np.array([[R[0][0]+R[1][1]+R[2][2],R[1][2]-R[2][1],R[2][0]-R[0][2],R[0][1]-R[1][0]],
       [R[1][2]-R[2][1],R[0][0]-R[1][1]-R[2][2],R[0][1]+R[1][0],R[0][2]+R[2][0]],
       [R[2][0]-R[0][2],R[0][1]+R[1][0],-R[0][0]+R[1][1]-R[2][2],R[1][2]+R[2][1]],
       [R[0][1]-R[1][0],R[0][2]+R[2][0],R[1][2]+R[2][1],-R[0][0]-R[1][1]+R[2][2]]
       ])
    print(F)
    V,D=np.linalg.eig(F)
    ev=V[0]
    evv=D[:,0]
    for i in range(1,4):
        if V[i]>ev:
            ev=V[i]
            evv=D[:,i]
    evv=evv.tolist()
    print(evv)
    return reser(X,evv)

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

if __name__=="__main__":
    m=os.getcwd()+"\\data\\transform\\masterlocal-1.csv"
    m_a,m_matrix=readAccelerationMatrix(m)
    m_a=np.mat(m_a[:200]).transpose()
    s=os.getcwd()+"\\data\\transform\\slavelocal-1.csv"
    s_a,s_matrix=readAccelerationMatrix(s)
    s_a=np.mat(s_a[:200]).transpose()
    data=residuum(m_a,s_a)
    output(m,data)