import scipy.io as sp
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fft

# fh = open("/home/g/Desktop/Full Duplex 6001/Results/multi_sine/tx_file", "rb")
# fh = open("/home/g/Desktop/Full Duplex 6001/Results/multi_sine/rx_file", "rb")
fh = open("/home/g/Desktop/Full Duplex 6001/Results/multi_sine/y_clean_file", "rb")

y =np.fromfile(fh, dtype=float)
# print (y.shape)

x = np.arange(y.shape[0])
print (x.shape)

# start = 34000
# stop = 37000
start = 40000
stop = 60000
y1 = y[start:stop]
x1 = x[start:stop]

# ds = 2
# y1 = y[0:y.shape[0]:ds]
# x1 = x[0:y.shape[0]:ds]

y1f = fft.fft(y1)
x1f = np.arange(y1f.shape[0])
# x1f = np.linspace(0.0, 1.0/(2.0*T), size/2)

plt.figure(1)
plt.plot(x1,y1)

plt.figure(2)
plt.plot(x1f,y1f)


plt.show()