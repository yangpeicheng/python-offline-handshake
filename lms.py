import csv
import numpy as np
import math

NS2S = 1.0 / 1000000000.0
filename="D:\\SensorData\\master\\masterlocal-2.csv"
I=np.eye(3)
gravity=[]
gyroscope=[]
acceleration=[]
translated_acc=[]
timestamp=[]
pretime=0
current_matrix=I
with open(filename) as f:
    reader=csv.reader(f)
    for line in reader:
        if len(line)<16:
            break
        else:
            gravity.append(line)
            tempgravity=[float(i) for i in line[6:9]]
            tempgyro=[float(i) for i in line[3:6]]
            tempacc=[float(i) for i in line[9:12]]
            currentTime=long(line[15])
            if pretime==0:
                pretime=currentTime
                timestamp.append(0)
            else:
                dt=(currentTime-pretime)*NS2S
                timestamp.append(dt)
                pretime=currentTime
            current_matrix=updateMatrix(current_matrix,tempgyro,dt)
            gravity.append(tempgravity)
            gyroscope.append(tempgyro)
            acceleration.append(tempacc)


def updateMatrix(current,gyro,dt):
    delta=math.sqrt((gyro[0]*dt)*(gyro[0]*dt)+(gyro[1]*dt)*(gyro[1]*dt)+(gyro[2]*dt)*(gyro[2]*dt))
    B=np.array([[0,-gyro[2]*dt,gyro[1]*dt],
              [gyro[2]*dt,0,-gyro[0]*dt],
              [-gyro[1]*dt,gyro[0]*dt,0]
              ])
    B1=B*(math.sin(delta)/delta)
    B2=B*B*(1-math.cos(delta))/(delta*delta)
    m=I+B1+B2
    return current*m
