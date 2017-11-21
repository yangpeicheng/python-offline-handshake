import numpy as np
import os
import csv
from Utils import readAccelerationMatrix,align,shift_central
from matplotlib import pyplot as plt
import math


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

def calcR(X,Y):
    R = np.dot(X, Y.transpose())
    v,s,wt=np.linalg.svd(R)
    det=np.linalg.det(R)
    F_pos=np.array([[1,1,1],
                    [1,-1,-1],
                    [-1,1,-1],
                    [-1,-1,1]])
    F_neg=np.array([[1,1,-1],
                [1,-1,1],
                [-1,1,1],
                [-1,-1,-1]])
    if det>0:
        F=F_pos
    else:
        F=F_neg
    translated=np.dot(F,s.transpose()).tolist()
    best=translated.index(max(translated))
    mid=np.diag(F[best,])
    return np.dot(np.dot(wt.transpose(),mid),v.transpose())


def output(file,data):
    str=file.split('\\')
    str[-2]="RMSD"
    outputfile="\\".join(str)
    with open(outputfile,'w',newline="") as f:
        out=csv.writer(f)
        for i in data:
            out.writerow(i)

def outputGyro(file,data):
    str=file.split('\\')
    str[-2]="gyro"
    outputfile="\\".join(str)
    with open(outputfile,'w',newline="") as f:
        out=csv.writer(f)
        for i in data:
            out.writerow(i)

def getOrientationFromMatrix(R):
    values=[]
    values.append(math.atan2(R[1], R[4]))
    values.append(math.asin(-R[7]))
    values.append(math.atan2(-R[6], R[8]))
    return values

def matrix2quatern(R):
    R=np.transpose(R)
    K=np.zeros((4,4))
    K[0, 0] = (1 / 3) * (R[0, 0] - R[1, 1] - R[2, 2])
    K[0, 1] = (1 / 3) * (R[1, 0] + R[0, 1])
    K[0, 2] = (1 / 3) * (R[2, 0] + R[0, 2])
    K[0, 3] = (1 / 3) * (R[1, 2] - R[2, 1])
    K[1, 0] = (1 / 3) * (R[1, 0] + R[0, 1])
    K[1, 1] = (1 / 3) * (R[1, 1] - R[0, 0] - R[2, 2])
    K[1, 2] = (1 / 3) * (R[2, 1] + R[1, 2])
    K[1, 3] = (1 / 3) * (R[2, 0] - R[0, 2])
    K[2, 0] = (1 / 3) * (R[2, 0] + R[0, 2])
    K[2, 1] = (1 / 3) * (R[2, 1] + R[1, 2])
    K[2, 2] = (1 / 3) * (R[2, 2] - R[0, 0] - R[1, 1])
    K[2, 3] = (1 / 3) * (R[0, 1] - R[1, 0])
    K[3, 0] = (1 / 3) * (R[1, 2] - R[2, 1])
    K[3, 1] = (1 / 3) * (R[2, 0] - R[0, 2])
    K[3, 2] = (1 / 3) * (R[0, 1] - R[1, 0])
    K[3, 3] = (1 / 3) * (R[0, 0] + R[1, 1] + R[2, 2])
    [v,d]=np.linalg.eig(K)
    print(v)
    q=v[:4]
    return q

def matrix2axis(R):
    return [R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]]


def smoothAngular(pre,current):
    result=[]
    print(pre,current)
    for i in range(len(pre)):
        if current[i]-pre[i]>3:
            result.append(current[i]-2*math.pi)
        elif pre[i]-current[i]>3:
            result.append(current[i]+2*math.pi)
        else:
            result.append(current[i])
    return result


def calcGyro(R,matrix,p):
    gyro=[]
    pre=p.copy()
    for m in matrix:
        '''       t=np.dot(R,m).tolist()
               tt=[]
               for i in t:
                   tt.extend(i)
               s=getOrientationFromMatrix(tt)
               if len(pre)>0:
                   s=smoothAngular(pre,s)
               pre=s
               gyro.append(s)
           return shift_central(gyro)'''
        t=np.dot(R,m)
        q=matrix2axis(t)
        gyro.append(q)
    return gyro



def rotationByQuaternion(m,s):
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
    s_a = np.mat(s_a[:l]).transpose()
    testnum = int(l / 4)
    tm_a = m_a[:, :testnum]
    ts_a = s_a[:, :testnum]
    evv = residuum(tm_a, ts_a)
    data = reser(m_a, evv)
    output(m, data)
    output(s, s_a.transpose().tolist())

def rotationByMatrix(m,s):
    m_a, m_matrix = readAccelerationMatrix(m)
    s_a, s_matrix = readAccelerationMatrix(s)
    m_a = shift_central(m_a)
    s_a = shift_central(s_a)
    m_start, s_start = align(m, s)
    m_a = np.array(m_a[m_start:]).transpose()
    s_a = np.array(s_a[s_start:]).transpose()
    m_matrix=m_matrix[m_start:]
    s_matrix=s_matrix[s_start:]
    if m_a.shape[1] > s_a.shape[1]:
        l = s_a.shape[1]
    else:
        l = m_a.shape[1]
    m_a = m_a[:,:l]
    s_a = s_a[:,:l]
    m_matrix=m_matrix[:l]
    s_matrix=s_matrix[:l]
    trainNum = int(l / 4)
    train_m_a = m_a[:, :trainNum]
    train_s_a = s_a[:, :trainNum]
    R=calcR(train_m_a,train_s_a)
    translated=np.dot(R,m_a).transpose().tolist()
    gyro=calcGyro(R,m_matrix)
    sgyro=calcGyro(np.eye(3),s_matrix)
    output(m, translated)
    output(s, s_a.transpose().tolist())
    outputGyro(m,gyro)
    outputGyro(s,sgyro)

def splitRotate(m,s):
    m_a, m_matrix = readAccelerationMatrix(m)
    s_a, s_matrix = readAccelerationMatrix(s)
    m_a = shift_central(m_a)
    s_a = shift_central(s_a)
    m_start, s_start = align(m, s)
    m_a = np.array(m_a[m_start:]).transpose()
    s_a = np.array(s_a[s_start:]).transpose()
    m_matrix=m_matrix[m_start:]
    s_matrix=s_matrix[s_start:]
    if m_a.shape[1] > s_a.shape[1]:
        l = s_a.shape[1]
    else:
        l = m_a.shape[1]
    m_a = m_a[:,:l]
    s_a = s_a[:,:l]
    m_matrix=m_matrix[:l]
    s_matrix=s_matrix[:l]
    split_gap=100
    train_num=20
    train_start=0
    m_translated_acc=[]
    m_translated_gyro=[]
    pre=[0,0,0]
    while train_start<l:
        train_m_a = m_a[:, train_start:min(train_start+train_num,l)]
        train_s_a = s_a[:, train_start:min(train_start+train_num,l)]
        end=min(l,train_start+split_gap)
        R=calcR(train_m_a,train_s_a)
        m_translated_acc.extend(np.dot(R,m_a[:,train_start:end]).transpose().tolist())
        print(m)
        m_translated_gyro.extend(calcGyro(R,m_matrix[train_start:end],pre))
        pre=m_translated_gyro[-1]
        train_start+=split_gap
    output(m, m_translated_acc)
    output(s, s_a.transpose().tolist())
    outputGyro(m,m_translated_gyro)
    sgyro = calcGyro(np.eye(3), s_matrix,[0,0,0])
    outputGyro(s,sgyro)


def main_test():
    filepath = os.getcwd()+"\\data\\transform"
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"

    for i in range(1,26):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            m=os.path.join(filepath,mfile)
            s=os.path.join(filepath,sfile)
            splitRotate(m,s)

if __name__=="__main__":
    main_test()







    '''main_test()
    m=os.getcwd()+"\\data\\transform"+"\\masterlocal-15.csv"
    s=os.getcwd()+"\\data\\transform"+"\\slavelocal-15.csv"
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
    index=[0,75,205]
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
    output(s, s_a.transpose().tolist())'''