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
    k=2
    interval=50
    train_size=interval
    master_len=len(m_magnitude)
    slave_len=len(s_magnitude)
    aligned_master=[]
    aligned_slave=[]

    translated_master=[]
    translated_slave=[]
    count=0

    first=True
    while True:
        if first:
            train_size=100
            first=False
        else:
            train_size=20

        master_end=master_index+train_size
        slave_end=slave_index+train_size

        if master_end>=master_len or slave_end>=slave_len:
            l=min(max(master_end , master_len)-min(master_end , master_len),max(slave_end , slave_len)-min(slave_end , slave_len))
            aligned_master.extend(m_magnitude[master_index:master_index+l])
            aligned_slave.extend(s_magnitude[slave_index:slave_index+l])
            break
        count += 1
        m_start,s_start=align(m_magnitude[master_index:master_end],s_magnitude[slave_index:slave_end])

        if abs(m_start-s_start)>2:
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
    print(count*train_size/len(master_raw))
    return translated_master,translated_slave

def compareGraph(master,slave,label,f):
    plt.figure()
    plt.subplot(311)
    #print([master[i][0] for i in range(len(master))])
    labels=["device 1","device 2"]
    plt.plot([master[i][0] for i in range(len(master))],color='r')
    plt.plot([slave[i][0] for i in range(len(slave))],color='b')
    plt.ylabel(label[0])
    plt.legend(labels, fontsize=8)
    plt.subplot(312)
    plt.plot([master[i][1] for i in range(len(master))],color='r')
    plt.plot([slave[i][1] for i in range(len(slave))],color='b')
    plt.ylabel(label[1])
    plt.legend(labels, fontsize=8)
    plt.subplot(313)
    plt.plot([master[i][2] for i in range(len(master))],color='r')
    plt.plot([slave[i][2] for i in range(len(slave))],color='b')
    plt.ylabel(label[2])
    plt.xlabel("sample")
    plt.legend(labels, fontsize=8)


    plt.savefig(f)
    plt.clf()
    #plt.show()

def graphFromFile(m,s,label=["x","y","z"]):
    master=readAcc(m)
    slave=readAcc(s)
    f=m.split("\\")
    num=f[-1].split("-")[1].split(".")[0]
    f[-1]="picture"+"\\"+num+".jpg"
    figurename="\\".join(f)
    compareGraph(master,slave,label,figurename)

def test(masterfile,slavefile):
    m_a,m_g=readAccGyro(masterfile)
    s_a,s_g=readAccGyro(slavefile)

    tm,ts=adaptive_train(m_a,s_a)
    output(masterfile,tm,"AdaptiveAcc")
    output(slavefile,ts,"AdaptiveAcc")
    output(masterfile,Cartesian2Spherical(tm),"AdaptiveAccSph")
    output(slavefile,Cartesian2Spherical(ts),"AdaptiveAccSph")
    tmg,tsg=adaptive_train(m_g,s_g)
    output(masterfile,tmg,"AdaptiveGyro")
    output(slavefile,tsg,"AdaptiveGyro")
    output(masterfile,Cartesian2Spherical(tmg),"AdaptiveGyroSph")
    output(slavefile,Cartesian2Spherical(tsg),"AdaptiveGyroSph")
    return tm,ts

def output(file,data,f):
    str=file.split('\\')
    str[-2]=f
    #str[-2]="AdaptiveAcc"
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

    for i in range(1,45):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            m=os.path.join(filepath,mfile)
            s=os.path.join(filepath,sfile)
            test(m,s)

def batchGraph(file):
    filepath = os.getcwd() + "\\data\\"+file
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    for i in range(1,45):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            print(mfile)
            graphFromFile(os.path.join(filepath,mfile),os.path.join(filepath,sfile))

if __name__=="__main__":
    '''m,s=test(".\\data\\transform\\masterlocal-29.csv",".\\data\\transform\\slavelocal-29.csv")
    compareGraph(m,s)
    graphFromFile(".\\data\\RMSD\\masterlocal-29.csv",".\\data\\RMSD\\slavelocal-29.csv")'''
    #test(".\\data\\transform\\masterlocal-33.csv",".\\data\\transform\\slavelocal-33.csv")
    main_test()
    batchGraph("AdaptiveAccSph")
    #batchGraph("AdaptiveAcc")
    batchGraph("AdaptiveGyroSph")
    #batchGraph("AdaptiveGyro")
