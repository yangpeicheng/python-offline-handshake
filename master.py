import step
import os
import shutil

toPath="E:\SensorData\master"
fromPath="E:\SensorData\data"
index=0
for filename in os.listdir(toPath):
    num=int(filename.split('.',1)[0].split('-',1)[1])
    if num>index:
        index=num
index+=1
index_short=index
index_long=index
os.chdir(fromPath)
for filename in os.listdir(fromPath):
    print(filename)
    if len(filename)<15:
        newname="master"+filename.split('-',1)[0]+'-' +str(index_short)+".csv"
        index_short+=1
    else:
        newname = "master"+filename.split('-', 1)[0]+'-' + str(index_long)+".csv"
        index_long+=1
    print(newname)
    os.rename(filename,newname)
    shutil.move(fromPath+"\\"+newname,toPath)
os.chdir(toPath)
os.rmdir(fromPath)