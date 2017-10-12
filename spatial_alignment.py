import csv
import os
import numpy as np
from compare import pearson_correlation
import math
from subData import getMagnitude
from pca import align

def readAccMatrixGravity(filename):
    acceleration=[]
    matrix=[]
    gravity=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(0,3)])
            matrix.append(np.mat([float(line[x]) for x in range(3,12)]).reshape(3,3))
            gravity.append([float(line[x]) for x in range(12,15)])
    return acceleration,matrix,gravity

def translate(theta,g,data):
    matrix=initMatrix(theta,g)
    translate_data=[]
    for i in data:
        translate_data.append(np.dot(matrix,np.array(i).transpose()).tolist())
    return np.array(translate_data)

def norm(g):
    l=getMagnitude(g)
    return [i/l for i in g]

def cross_product(a,b):
    c=[0 for x in range(3)]
    c[0]=a[1]*b[2]-a[2]*b[1]
    c[1]=a[2]*b[0]-a[0]*b[2]
    c[2]=a[0]*b[1]-a[1]*b[0]
    return c

def initMatrix(theta,g):
    g=norm(g)
    r=1
    fi=math.pi/2-math.atan2(math.sqrt(g[0]*g[0]+g[1]*g[1]),g[2])
    x=convertFromSphericalToCardinal(r,fi,theta)
    y=norm(cross_product(g,x))
    return np.array([
        x,
        y,
        g
    ])


def compare(master,slave):
    m_start,s_start=align(master,slave)
    m_acc,m_matrix,m_g=readAccMatrixGravity(master)
    s_acc,s_matrix,s_g=readAccMatrixGravity(slave)
    m_acc=m_acc[m_start:]
    m_g=m_g[m_start:]
    s_acc=s_acc[s_start:]
    s_g=s_acc[s_start:]
    tr_m=translate(0,m_g[0],m_acc)
    n=20
    cor=-100
    final_theta=0
    for i in range(n):
        t=2*i/n*math.pi
        tr_s=translate(t,s_g[0],s_acc)
        correlation=[pearson_correlation(tr_m[:,j],tr_s[:,j]) for j in range(3)]
        if sum(correlation)>cor:
            cor=sum(correlation)
            final_theta=t
            best_cor=correlation
        #print(correlation)
    print(final_theta,best_cor)
    output(master,tr_m)
    output(slave,translate(final_theta,s_g[0],s_acc))


def output(file,data):
    str=file.split('\\')
    str[-2]="MSE"
    outputfile="\\".join(str)
    with open(outputfile,'w',newline="") as f:
        out=csv.writer(f)
        for i in data:
            out.writerow(i)



def convertFromSphericalToCardinal(r,fi,theta):
    x = r * math.sin(fi) * math.cos(theta)
    y = r * math.sin(fi) * math.sin(theta)
    z = r * math.cos(fi)
    return [x,y,z]

if __name__=="__main__":
    filepath=os.getcwd()+"\\data\\transform"
    compare(os.path.join(filepath,"masterlocal-8.csv"),os.path.join(filepath,"slavelocal-8.csv"))