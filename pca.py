from sklearn.decomposition import PCA
import csv
import math
import numpy as np
import os
from compare import pearson_correlation
from subData import getMagnitude

def  pcaTrain(data,filename):
    pca=PCA(n_components=3)
    pca.fit(data[0:50])
    with open("E:\SensorData\pca\\variance_ratio.txt",'a') as f:
        f.writelines(filename+'\r\n')
        tmp=[str(pca.explained_variance_ratio_[i]) for i in range(3)]
        f.writelines(",".join(tmp)+'\r\n')
    '''print(pca.explained_variance_ratio_)
    print(pca.explained_variance_)
    print(pca.components_)'''
    return pca.components_

def transform(data,components):
    mean=[0,0,0]
    for line in data:
        for j in range(3):
            mean[j]+=line[j]
    mean=[mean[i]/len(data) for i in range(3)]
    for i in range(len(data)):
        for j in range(3):
            data[i][j]-=mean[j]
    ans=[]
    for line in data:
        #ans.append([dot_product(line,components[0]),dot_product(line,components[1]),dot_product(line,components[2])])
        ans.append([dot_product(line,components[x]) for x in range(3)])
    return ans



def readData(filename):
    data=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            data.append([float(x) for x in line])
    return data

def readAccelerationMatrix(filename):
    acceleration=[]
    matrix=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            acceleration.append([float(line[x]) for x in range(0,3)])
            matrix.append(np.mat([float(line[x]) for x in range(3,12)]).reshape(3,3))
    return acceleration,matrix

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





def getGlobalData(filename,start):
    acceleration,matrix=readAccelerationMatrix(filename)
    acceleration=acceleration[start:]
    matrix=matrix[start:]
    m_components=pcaTrain(acceleration,filename)
    global_acceleration=transform(acceleration,m_components)
    angular=[]
    current=m_components
    pre=[]
    for m in matrix:
        tmp=[]
        for i in np.dot(current,m).tolist():
            tmp=tmp+i
        print(tmp)
        s=getOrientationFromMatrix(tmp)
        if len(pre)>0:
            s=smoothAngular(pre,s)
        pre = s
        angular.append(s)
    str=filename.split('\\')
    str[-2]="pca"
    outputfile="\\".join(str)
    output=open(outputfile,"w",newline="")
    writer=csv.writer(output)
    for i in range(len(global_acceleration)):
        writer.writerow(global_acceleration[i]+angular[i])
    return global_acceleration,angular

def smoothAngular(pre,current):
    result=[]
    for i in range(len(pre)):
        if current[i]-pre[i]>4:
            result.append(current[i]-2*math.pi)
        elif pre[i]-current[i]>4:
            result.append(current[i]+2*math.pi)
        else:
            result.append(current[i])
    return result

'''def test(m,s):
    m_data=readData(m)
    s_data=readData(s)
    m_components=pcaTrain(m_data)
    s_components=pcaTrain(s_data)
    m_test_data=np.mat(transform(m_data[0:50],m_components))
    s_test_data=np.mat(transform(s_data[0:50],s_components))
    test_correlation=pearson_correlation(m_test_data[:,0],s_test_data[:,0])
    print(test_correlation)
    if test_correlation<0:
        s_components=0-s_components
    m_final_data=transform(m_data,m_components)
    writeData(m.split('.')[0]+"transform.csv",m_final_data)
    s_final_data=transform(s_data,s_components)
    writeData(s.split('.')[0]+"transform.csv",s_final_data)
    result=[pearson_correlation(np.mat(m_final_data)[:,i],np.mat(s_final_data)[:,i]) for i in range(3)]
    print(result)
    return result'''

def writeData(filename,data):
    with open(filename,'w',newline="") as f:
        write=csv.writer(f)
        for line in data:
            write.writerow(line)

'''def transformGyro(accFilename,gyroFilename):
    accdata,pcacomponents=transform(accFilename)
    arraycomponents=[]
    for lines in pcacomponents:
        for i in lines:
            arraycomponents.append(-i)
    output=open(gyroFilename.split(".")[0]+"pca.csv","w",newline="")
    write=csv.writer(output)
    with open(gyroFilename) as f:
        reader=csv.reader(f)
        for lines in reader:
            tmp=[float(x) for x in lines]
            write.writerow(getOrientationFromMatrix(matrixMultiple(arraycomponents,tmp)))'''



def dot_product(x,y):
    s=0.0
    for i in range(len(x)):
        s+=float(x[i])*y[i]
    return s

def getOrientationFromMatrix(R):
    values=[]
    values.append(math.atan2(R[1], R[4]))
    values.append(math.asin(-R[7]))
    values.append(math.atan2(-R[6], R[8]))
    return values

def instanceOfPca():
    filepath = os.getcwd()+"\\data\\transform"
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,13):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            mfilename=os.path.join(filepath,mfile)
            sfilename=os.path.join(filepath,sfile)
            mstart,sstart=align(mfilename,sfilename)
            getGlobalData(mfilename,mstart)
            getGlobalData(sfilename,sstart)

if __name__=="__main__":
    filepath = os.getcwd() + "\\data\\transform"
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,13):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            mfilename=os.path.join(filepath,mfile)
            sfilename=os.path.join(filepath,sfile)
            mstart,sstart=align(mfilename,sfilename)
            getGlobalData(mfilename,mstart)
            getGlobalData(sfilename,sstart)