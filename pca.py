from sklearn.decomposition import PCA
import csv
import math
import numpy as np

def  pcaTrain(data):
    pca=PCA(n_components=3)
    pca.fit(data[0:50])
    print(pca.explained_variance_ratio_)
    print(pca.explained_variance_)
    print(pca.components_)
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
        ans.append([dot_product(line,components[0]),dot_product(line,components[1]),dot_product(line,components[2])])
    return ans

def readData(filename):
    data=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for line in reader:
            data.append([float(x) for x in line])
    return data

def test(m,s):
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
    return result

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



def pearson_correlation(x,y):
    mean_x=sum(x)/len(x)
    mean_y=sum(y)/len(y)
    lxx=0
    lyy=0
    lxy=0
    for i in range(min(len(x),len(y))):
        lxy+=(x[i]-mean_x)*(y[i]-mean_y)
        lxx+=(x[i]-mean_x)*(x[i]-mean_x)
        lyy+=(y[i]-mean_y)*(y[i]-mean_y)
    return lxy/math.sqrt(lxx*lyy)


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

def matrixMultiple(a,b):
    result=[0 for i in range(9)]
    result[0] = a[0] * b[0] + a[1] * b[3] + a[2] * b[6]
    result[1] = a[0] * b[1] + a[1] * b[4] + a[2] * b[7]
    result[2] = a[0] * b[2] + a[1] * b[5] + a[2] * b[8]

    result[3] = a[3] * b[0] + a[4] * b[3] + a[5] * b[6]
    result[4] = a[3] * b[1] + a[4] * b[4] + a[5] * b[7]
    result[5] = a[3] * b[2] + a[4] * b[5] + a[5] * b[8]

    result[6] = a[6] * b[0] + a[7] * b[3] + a[8] * b[6]
    result[7] = a[6] * b[1] + a[7] * b[4] + a[8] * b[7]
    result[8] = a[6] * b[2] + a[7] * b[5] + a[8] * b[8]

    return result;
#filename="E:\\SensorData\\ouput\\m1t.csv"
#ransform(filename)
#test("E:\\SensorData\\ouput\\m1t.csv","E:\\SensorData\\ouput\\s1t.csv")
if __name__=="__main__":
    test("E:\\SensorData\\pcatest\\masterlocal-9tt.csv","E:\\SensorData\\pcatest\\slavelocal-9tt.csv")
#transform("E:\\SensorData\\ouput\\masterlocal-3tt.csv")
#transformGyro("E:\\SensorData\\ouput\\masterlocal-2tt.csv","E:\\SensorData\\ouput\\masterlocal-2tgyro.csv")
#transformGyro("E:\\SensorData\\ouput\\slavelocal-2tt.csv","E:\\SensorData\\ouput\\slavelocal-2tgyro.csv")