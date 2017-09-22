from pca import readData
import numpy as np
import matplotlib.pyplot as plt

filename="E:\\SensorData\\pcatest\\masterlocal-9tttransform.csv"
data=np.mat(readData(filename))[:,0]
x=0.02*np.linspace(0,len(data),len(data))
#plt.plot(x,data)

n=len(data)
freq=(np.arange(n)*0.02)[:int(n/2)]
frequence_data=np.abs(np.fft.rfft(data))[:int(n/2)]
plt.plot(freq,frequence_data)
plt.show()

'''sampling_rate = 8000
fft_size = 512
t = np.arange(0, 1.0, 1.0/sampling_rate)
x = np.sin(2*np.pi*156.25*t)  + 2*np.sin(2*np.pi*234.375*t)
xs = x[:fft_size]
xf = np.fft.rfft(xs)/fft_size
freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
plt.figure(figsize=(8,4))
plt.subplot(211)
plt.plot(t[:fft_size], xs)
plt.xlabel(u"时间(秒)")
plt.title(u"156.25Hz和234.375Hz的波形和频谱")
plt.subplot(212)
plt.plot(freqs, xfp)
plt.xlabel(u"频率(Hz)")
plt.subplots_adjust(hspace=0.4)
plt.show()'''
