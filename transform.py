import numpy as np
import math
import csv
import os
def updateMatrix(currentMatrix,gyro,dt):
    delta = math.sqrt(dt * dt * (gyro[0] * gyro[0] + gyro[1] * gyro[1] + gyro[2] * gyro[2]))
    B=np.array(
        [[0,-gyro[2]*dt,gyro[1]*dt],
        [gyro[2]*dt,0,-gyro[0]*dt],
        [-gyro[1]*dt,gyro[0]*dt,0]]
    )
    B1=(math.sin(delta)/delta)*B
    B2=((1-math.cos(delta))/(delta*delta))*np.dot(B,B)
    matrix=np.eye(3)+B1+B2
    currentMatrix=np.dot(currentMatrix,matrix)
    return currentMatrix

def handler(m):
    NS2S = 1.0 / 1000000000.0
    acceleration=[]
    matrix=[]
    gyroscope=[]
    current=np.eye(3)
    last_timestamp=0
    with open(m) as f:
        reader=csv.reader(f)
        for line in reader:
            time=int(line[15])
            if last_timestamp>0 and time!=last_timestamp:
                gyro=np.array([float(line[i]) for i in range(9,12)])
                lineacc=np.array([float(line[i]) for i in range(3,6)]).transpose()
                #g=[float(line[i]) for i in range(9,12)]
                dt=(time-last_timestamp)*NS2S
                current=updateMatrix(current,gyro,dt)
                acceleration.append(np.dot(current,lineacc).tolist())
                matrix.append(current.tolist())
                gyroscope.append(np.dot(current,gyro).tolist())
            last_timestamp=time
    s=m.split('\\')
    s[-2]="transform"
    newfile='\\'.join(s)
    with open(newfile,'w',newline="") as f:
        writer=csv.writer(f)
        for i in range(len(acceleration)):
            tmp=[]
            for j in range(3):
                tmp=tmp+matrix[i][j]
            tmp=tmp+gyroscope[i]
            writer.writerow(acceleration[i]+tmp)
    return acceleration,matrix

def instanceOfTransform():
    filepath=os.getcwd()+"\\data\\handshake"
    files=os.listdir(filepath)
    for f in files:
        filename=os.path.join(filepath,f)
        print(filename)
        handler(filename)

if __name__=="__main__":
    instanceOfTransform()