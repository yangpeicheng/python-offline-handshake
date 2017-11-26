from Utils import readAccelerationMatrix,getMagnitude,shift_central,readAcc,readAccGyro
from time_alignment import align
from matplotlib import pyplot as plt
import csv
from RMSD import calcR,Cartesian2Spherical
import numpy as np
import os

def adaptive_train(master_raw,slave_raw):

    master=shift_central(master_raw)
    slave=shift_central(slave_raw)

    m_magnitude=[getMagnitude(master[i]) for i in range(len(master))]
    s_magnitude=[getMagnitude(slave[i]) for i in range(len(slave))]

    master=np.array(master).transpose()
    slave=np.array(slave).transpose()


    master_index=0
    slave_index=0
    k=1
    interval=100
    train_size=interval
    master_len=len(m_magnitude)
    slave_len=len(s_magnitude)
    aligned_master=[]
    aligned_slave=[]

    translated_master=[]
    translated_slave=[]
    count=0
    while True:
        master_end=master_index+train_size
        slave_end=slave_index+train_size

        if master_end>=master_len or slave_end>=slave_len:
            l=min(max(master_end , master_len)-min(master_end , master_len),max(slave_end , slave_len)-min(slave_end , slave_len))
            aligned_master.extend(m_magnitude[master_index:master_index+l])
            aligned_slave.extend(s_magnitude[slave_index:slave_index+l])
            break
        count += 1
        m_start,s_start=align(m_magnitude[master_index:master_end],s_magnitude[slave_index:slave_end])

        if abs(m_start-s_start)>5:
            k=1
            master_index+=m_start
            slave_index+=s_start
        else:
            k+=1
        #print(k,train_size)
        #print(master_index,slave_index)
        if master_index>=master_len or slave_index>=slave_len:
            break

        l = min(k * interval, master_len - master_index, slave_len - slave_index)

        m_tmp_end=master_index+l
        s_tmp_end=slave_index+l
        aligned_master.extend(m_magnitude[master_index:m_tmp_end])
        aligned_slave.extend(s_magnitude[slave_index:s_tmp_end])

        l=min(slave_end-slave_index,master_end-master_index)
        R=calcR(master[:,master_index:master_index+l],slave[:,slave_index:slave_index+l])
        translated_master.extend(np.dot(R,master[:,master_index:m_tmp_end]).transpose().tolist())
        translated_slave.extend((slave[:,slave_index:s_tmp_end]).transpose().tolist())


        master_index=m_tmp_end
        slave_index=s_tmp_end

    #compareGraph(master_raw,slave_raw)
    #compareGraph(translated_master,translated_slave)
    print(count*train_size)
    return translated_master,translated_slave

def compareGraph(master,slave):
    plt.figure()
    plt.subplot(311)
    #print([master[i][0] for i in range(len(master))])
    labels=["device 1","device 2"]
    plt.plot([master[i][0] for i in range(len(master))],color='r')
    plt.plot([slave[i][0] for i in range(len(slave))],color='b')
    plt.ylabel("x")
    plt.legend(labels)
    plt.subplot(312)
    plt.plot([master[i][1] for i in range(len(master))],color='r')
    plt.plot([slave[i][1] for i in range(len(slave))],color='b')
    plt.ylabel("y")
    plt.legend(labels)
    plt.subplot(313)
    plt.plot([master[i][2] for i in range(len(master))],color='r')
    plt.plot([slave[i][2] for i in range(len(slave))],color='b')
    plt.ylabel("z")
    plt.xlabel("sample")
    plt.legend(labels)
    plt.show()

def graphFromFile(m,s):
    master=readAcc(m)
    slave=readAcc(s)
    compareGraph(master,slave)

def test(masterfile,slavefile):
    m_a,m_g=readAccGyro(masterfile)
    s_a,s_g=readAccGyro(slavefile)

    tm,ts=adaptive_train(m_a,s_a)
    output(masterfile,Cartesian2Spherical(tm))
    output(slavefile,Cartesian2Spherical(ts))
    tmg,tsg=adaptive_train(m_g,s_g)
    outputGyro(masterfile,Cartesian2Spherical(tmg))
    outputGyro(slavefile,Cartesian2Spherical(tsg))
    return tm,ts

def output(file,data):
    str=file.split('\\')
    str[-2]="AdaptiveAccSph"
    outputfile="\\".join(str)
    with open(outputfile,'w',newline="") as f:
        out=csv.writer(f)
        for i in data:
            out.writerow(i)

def outputGyro(file,data):
    str=file.split('\\')
    str[-2]="AdaptiveGyroSph"
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

    for i in range(1,40):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            m=os.path.join(filepath,mfile)
            s=os.path.join(filepath,sfile)
            test(m,s)

if __name__=="__main__":
    '''m,s=test(".\\data\\transform\\masterlocal-29.csv",".\\data\\transform\\slavelocal-29.csv")
    compareGraph(m,s)
    graphFromFile(".\\data\\RMSD\\masterlocal-29.csv",".\\data\\RMSD\\slavelocal-29.csv")'''
    main_test()
    #graphFromFile(".\\data\\RMSD\\masterlocal-29.csv", ".\\data\\RMSD\\slavelocal-29.csv")
    #graphFromFile(".\\data\\adaptive\\masterlocal-29.csv", ".\\data\\adaptive\\slavelocal-29.csv")
