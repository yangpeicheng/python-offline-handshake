from Utils import readAcc
from matplotlib import pyplot as plt

def test(a,b):
    a_bits,a_error=getPartial(a)
    b_bits,b_error=getPartial(b)
    plt.figure()
    labels=["Cartesian ","Spherical"]
    plt.subplot(211)
    print(a_bits)
    x=range(len(a_bits))
    plt.plot(x,a_bits,color='r',marker='o', mec='r', mfc='w')
    plt.plot(x,b_bits,color='b',marker='o', mec='b', mfc='w')
    plt.ylabel("# of bits")
    plt.legend(labels, fontsize=8)
    plt.subplot(212)
    plt.plot(x,a_error,color='r',marker='o', mec='r', mfc='w')
    plt.plot(x,b_error,color='b',marker='o', mec='b', mfc='w')
    plt.ylabel("error")
    plt.legend(labels,fontsize=8)
    plt.show()




def getPartial(data):
    tbits=[line[1] for line in data][25:]
    bits=tbits[-5::]
    bits.extend(tbits[:-5:])
    terror=[line[2] for line in data][25:]
    error=terror[-5::]
    error.extend(terror[:-5:])
    return bits,error

def getCor(data):
    tfirst=[line[1] for line in data][25:]
    first=tfirst[-5::]
    first.extend(tfirst[:-5:])
    tbits=[line[1] for line in data][25:]
    bits=tbits[-5::]
    bits.extend(tbits[:-5:])
    terror=[line[2] for line in data][25:]
    error=terror[-5::]
    error.extend(terror[:-5:])
    return tfirst,bits,error

def draw_cor(a,b):
    a_x, a_y,a_z = getCor(a)
    b_x, b_y, b_z = getCor(b)
    plt.figure()
    labels = ["Cartesian ", "Spherical"]
    plt.subplot(311)
    x = range(len(a_x))
    plt.plot(x, a_x, color='r', marker='o', mec='r', mfc='w')
    plt.plot(x, b_x, color='b', marker='o', mec='b', mfc='w')
    plt.ylabel("x")
    plt.legend(labels, fontsize=8)
    plt.subplot(312)
    plt.plot(x, a_y, color='r', marker='o', mec='r', mfc='w')
    plt.plot(x, b_y, color='b', marker='o', mec='b', mfc='w')
    plt.ylabel("y")
    plt.legend(labels, fontsize=8)
    plt.subplot(313)
    plt.plot(x, a_z, color='r', marker='o', mec='r', mfc='w')
    plt.plot(x, b_z, color='b', marker='o', mec='b', mfc='w')
    plt.ylabel("z")
    plt.legend(labels, fontsize=8)
    plt.show()

rmsd=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\RMSD\\result.csv")
gyro=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\gyro\\result.csv")
AccSpherical=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\AccSpherical\\result.csv")
GyroSpherical=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\GyroSpherical\\result.csv")
AdaptiveAcc=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAcc\\result.csv")
AdaptiveAccSph=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveAccSph\\result.csv")
AdaptiveGyro=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveGyro\\result.csv")
AdaptiveGyroSph=readAcc("C:\\Users\\10959\Desktop\python-offline-handshake\data\AdaptiveGyroSph\\result.csv")

draw_cor(AdaptiveGyro,AdaptiveGyroSph)

