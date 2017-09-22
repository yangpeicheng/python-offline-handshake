import csv
import math
import matplotlib.pyplot as plt

def getBits(filename="E:\\SensorData\\slave\\slaveglobalLocal-1.csv"):
    data=[[],[],[]]
    ALPHA=0.3
    bits=[]
    with open(filename,'rb') as f:
        read=csv.reader(f)
        for line in read:
            for i in range(3):
                data[i].append(float(line[i]))
    average=[sum(data[x])/len(data[x]) for x in range(3)]
    variance=[0 for i in range(3)]
    for i in range(3):
        for j in range(len(data[i])):
            variance[i]+=(data[i][j]-average[i])*(data[i][j]-average[i])

    for v in range(len(variance)):
        variance[v]=math.sqrt(variance[v]/len(data[0]))

    for i in range(3):
        up=average[i]+ALPHA*variance[i]
        low=average[i]-ALPHA*variance[i]
        for val in data[i]:
            if val>up:
                bits.append(1)
            elif val<low:
                bits.append(0)
            else:
                bits.append(2)
    return bits
#print data,average
def getExcursionIndex(bits,m=3):
    index=[]
    pre=bits[0]
    consecutive=1
    for i in range(1,len(bits)):
        if bits[i]!=2 and bits[i]==pre:
            consecutive+=1
        else:
            if consecutive>=m:
                index.append((2*i-(consecutive+1))/2)
            consecutive=1
            pre=bits[i]
        if i==len(bits)-1 and consecutive>=m:
            index.append((2*i-consecutive+1)/2)
    return index

def salveIndex(bits,index,m=3):
    result=[]
    for i in index:
        bit=bits[i]
        start=i-m/2+1
        end=i+m/2
        flag=True
        for j in range(start,end+1):
            if bits[j]==2 or bits[j]!=bit:
                flag=False
                break
        if flag:
            result.append(i)
    return result


masterbits=getBits("E:\\SensorData\\master\\masterglobalLocal-1.csv")
slavebits=getBits("E:\\SensorData\\slave\\slaveglobalLocal-1.csv")

#mm=[masterbits[i] for i in getExcursionIndex(masterbits,5)]
#ss=[slavebits[i] for i in getExcursionIndex(masterbits,5)]

mIndex=getExcursionIndex(masterbits)
sIndex=salveIndex(slavebits,mIndex)
print mIndex
print sIndex
print [masterbits[i] for i in sIndex]
print [slavebits[i] for i in sIndex]
#plt.plot(slavebits,color='red')
#plt.show()