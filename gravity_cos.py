import numpy as np
from Utils import readGravity
from matplotlib import pyplot as plt


def calc_cos(start,data):
    return np.arccos(np.dot(start,data)/(np.linalg.norm(start)*np.linalg.norm(data)))/np.pi*180

def test(filename):
    data=readGravity(filename)
    start=data[0]
    result=[]
    for i in data:
        result.append(calc_cos(start,i))
    plt.plot(result)
    plt.show()


if __name__=="__main__":
    num=str(50)
    test(".\\data\\master\\masterlocal-"+num+".csv")