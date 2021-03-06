from Utils import pearson_correlation,readAcc,getMagnitude,shift_central,readAll
from matplotlib import pyplot as plt
import os
import csv

def output(data,file):
    with open(file,'w',newline="") as f:
        writer=csv.writer(f)
        for line in data:
            writer.writerow(line)


def align(master,slave):
    le=len(master)
    l=int(len(master)*4/9)
    m_start=0
    s_start=0
    correlation=0
    for i in range(le-l):
        for j in range(le-l):
            tmp_cor=pearson_correlation(master[i:i+l],slave[j:j+l])
            if tmp_cor>correlation:
                correlation=tmp_cor
                m_start=i
                s_start=j
    return m_start,s_start

def align_beginning(master,slave):
    master_acc=readAll(master)
    slave_acc=readAll(slave)
    master_acc=shift_central(master_acc)
    slave_acc=shift_central(slave_acc)
    m_magnitude=[getMagnitude(master_acc[i][:3]) for i in range(len(master_acc))]
    s_magnitude=[getMagnitude(slave_acc[i][:3]) for i in range(len(slave_acc))]
    m_start,s_start=align(m_magnitude[:200],s_magnitude[:200])
    l=min(len(m_magnitude)-m_start,len(s_magnitude)-s_start)
    return master_acc[m_start:m_start+l],slave_acc[s_start:s_start+l]

def batch_align(file="transform"):
    filepath = os.getcwd() + "\\data\\"+file
    files=os.listdir(filepath)
    master="masterlocal"
    slave="slavelocal"
    outputpath=os.getcwd() + "\\data\\"+"aligned"
    for i in range(26,45):
        mfile=master+"-"+str(i)+".csv"
        sfile=slave+"-"+str(i)+".csv"
        if mfile in files and sfile in files:
            print(mfile)
            m,s=align_beginning(os.path.join(filepath,mfile),os.path.join(filepath,sfile))
            output_m=os.path.join(outputpath,mfile)
            output_s=os.path.join(outputpath,sfile)
            output(m,output_m)
            output(s,output_s)


def time_alignment(master,slave):
    master_index=0
    slave_index=0
    k=2
    interval=50
    master_len=len(master)
    slave_len=len(slave)

    aligned_master=[]
    aligned_slave=[]

    first=True
    while True:
        if first:
            train_size=75
            first=False
        else:
            train_size=20
        master_end=master_index+train_size
        slave_end=slave_index+train_size
        if master_end>=master_len or slave_end>=slave_len:

            l=min(master_end-master_index,master_len-master_index,slave_end-slave_index,slave_len-slave_index)
            aligned_master.extend(master[master_index:master_index+l])
            aligned_slave.extend(slave[slave_index:slave_index+l])
            break

        m_start,s_start=align(master[master_index:master_end],slave[slave_index:slave_end])
        print(m_start,s_start)
        #if m_start>2 or s_start>2:
        if abs(m_start-s_start)>2:
            k=1
            master_index+=m_start
            slave_index+=s_start
        else:
            k+=1
            #train_size=max(int(train_size/4),10)
        #print(k,train_size)
        if master_index>=master_len or slave_index>=slave_len:
            break
        l = min(k * interval, master_len - master_index, slave_len - slave_index)
        aligned_master.extend(master[master_index:master_index+l])
        aligned_slave.extend(slave[slave_index:slave_index+l])
        #print("len", len(aligned_master), len(aligned_slave))

        master_index=min(master_index+k*interval,master_len)
        slave_index=min(slave_index+k*interval,slave_len)
        #print(master_index,slave_index)

    print(pearson_correlation(aligned_master,aligned_slave))

    return aligned_master,aligned_slave

def period_alignment(master,slave):
    master_index=0
    slave_index=0
    interval=300
    train_size=100
    master_len=len(master)
    slave_len=len(slave)

    aligned_master=[]
    aligned_slave=[]

    while True:
        master_end=master_index+train_size
        slave_end=slave_index+train_size

        if master_end>=master_len or slave_end>=slave_len:

            l=min(master_end-master_index,master_len-master_index,slave_end-slave_index,slave_len-slave_index)
            aligned_master.extend(master[master_index:master_index+l])
            aligned_slave.extend(slave[slave_index:slave_index+l])
            break

        m_start,s_start=align(master[master_index:master_end],slave[slave_index:slave_end])
        print(m_start,s_start)
        #if m_start>2 or s_start>2:
        if abs(m_start-s_start)>2:
            master_index+=m_start
            slave_index+=s_start
            #train_size=max(int(train_size/4),10)
        #print(k,train_size)
        if master_index>=master_len or slave_index>=slave_len:
            break
        l = min( interval, master_len - master_index, slave_len - slave_index)
        aligned_master.extend(master[master_index:master_index+l])
        aligned_slave.extend(slave[slave_index:slave_index+l])
        #print("len", len(aligned_master), len(aligned_slave))

        master_index=min(master_index+interval,master_len)
        slave_index=min(slave_index+interval,slave_len)
        #print(master_index,slave_index)

    print(pearson_correlation(aligned_master,aligned_slave))

    return aligned_master,aligned_slave

def magnitudeGraph(aligned_master,aligned_slave,master,slave):
    label=["device 1","device 2"]
    plt.figure()
    plt.subplot(211)
    plt.plot(aligned_master,color='r')
    plt.plot(aligned_slave,color='b')
    plt.ylabel("Adaptive alignment")
    #plt.legend(label)
    plt.subplot(212)
    plt.plot(master,color='r')
    plt.plot(slave,color='b')
    plt.xlabel("sample")
    plt.ylabel("Beginning alignment")
    #plt.legend(label)
    plt.show()

def test(master,slave,m,s):
    master_acc=readAcc(master)
    slave_acc=readAcc(slave)
    master_acc=shift_central(master_acc)
    slave_acc=shift_central(slave_acc)
    m_magnitude=[getMagnitude(master_acc[i]) for i in range(len(master_acc))]
    s_magnitude=[getMagnitude(slave_acc[i]) for i in range(len(slave_acc))]
    print("pearson",pearson_correlation(m_magnitude,s_magnitude))
    align_master,align_slave=time_alignment(m_magnitude,s_magnitude)


    mm=[getMagnitude(m[i]) for i in range(len(m))]
    sm=[getMagnitude(s[i]) for i in range(len(s))]
    print("pearson", pearson_correlation(mm, sm))
    magnitudeGraph(align_master,align_slave,mm,sm)


if __name__=="__main__":
    '''num=str(14)
    m=readAcc(".\\data\\RMSD\\masterlocal-"+num+".csv")
    s=readAcc(".\\data\\RMSD\\slavelocal-"+num+".csv")
    test(".\\data\\transform\\masterlocal-"+num+".csv",".\\data\\transform\\slavelocal-"+num+".csv",m,s)'''
    batch_align()
