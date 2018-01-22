from statsmodels.tsa.stattools import acf,pacf
from matplotlib import pyplot as plt
from quantization import compareByLevelcrossing

def plotPacf(data):
    '''x=data[:int(len(data)/3)]
    y=data[int(len(data)/3):2*int(len(data)/3)]
    z=data[2*int(len(data)/3):]
    xlag_pacf=pacf(x,nlags=20)
    ylag_pacf = pacf(y, nlags=20)
    zlag_pacf = pacf(z, nlags=20)
    plt.subplot(311)
    plt.plot(xlag_pacf)
    plt.subplot(312)
    plt.plot(ylag_pacf)
    plt.subplot(313)
    plt.plot(zlag_pacf)
    plt.show()'''
    lag_pacf=pacf(data,nlags=10)
    plt.plot(lag_pacf)
    plt.show()

def test(mfile,sfile):
    key,b,c=compareByLevelcrossing(mfile,sfile)
    plotPacf(key)


if __name__=="__main__":
    test("C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAcc\\masterlocal-31.csv","C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAcc\\slavelocal-31.csv")
