import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import scipy.fftpack as fftp
import os
import sys

# print (sys.argv)
file = ['tx_file', 'rx_file', 'y_clean_file']
dir_path = os.path.dirname(os.path.realpath(__file__))


fh = open(dir_path + "/" + file[0], "rb")
tx = np.fromfile(fh, dtype=float)

fh = open(dir_path + "/" + file[1], "rb")
rx = np.fromfile(fh, dtype=float)

fh = open(dir_path + "/" + file[2], "rb")
rx_clean = np.fromfile(fh, dtype=float)

x = np.arange(tx.shape[0])
# print (x.shape)

buffsize = 20440
g = 6
start = buffsize * 5
stop = start + int(g * buffsize )
# start = 34000
# stop = 37000
# start = 40000
# stop = 60000


x1 = x[start:stop]
tx1 = tx[start:stop]
rx1 = rx[start:stop]
rx_clean1 = rx_clean[start:stop]


# tx1f = buffsize * 2 * np.absolute(fft.fftshift(fft.fft(tx1) / x1.shape[0]))
# rx1f = buffsize * 2 * np.absolute(fft.fftshift(fft.fft(rx1) / x1.shape[0]))
# rx_clean1f = buffsize * 2 * np.absolute(fft.fftshift(fft.fft(rx_clean1) / x1.shape[0]))

tx1f = np.absolute(fftp.fftshift(fftp.fft(tx1)))
rx1f = np.absolute(fftp.fftshift(fftp.fft(rx1)))
rx_clean1f = np.absolute(fftp.fftshift(fftp.fft(rx_clean1)))

x1f = fftp.fftfreq(tx1f.size, 1/2000000)

log_tx1f = 10 * np.log10(1000 * (tx1f ** 2) / 100)
log_rx1f = 10 * np.log10(1000 * (rx1f ** 2) / 100)
log_rx_clean1f = 10 * np.log10(1000 * (rx_clean1f ** 2) / 100)

# bw = 5 * 10 ** 5
# step = 2 * bw / tx1f.shape[0]
# x1f = np.arange(- bw, bw, step)

# print (tx1f.shape, rx1f.shape, rx_clean1f.shape, x1f.shape)

# plt.figure(1)
# plt.plot(x1, tx1, 'r', x1, rx1, 'b', x1, rx_clean1, 'g', alpha=0.5)

# red_patch = ptch.Patch(color='r', label='TX')
# blue_patch = ptch.Patch(color='b', label='RX')
# green_patch = ptch.Patch(color='g', label='RX Clean')
# plt.legend(handles=[red_patch, blue_patch, green_patch])


plt.figure(2)
plt.plot(x1f/1000, log_tx1f, 'r', x1f/1000, log_rx1f, 'b', x1f/1000, log_rx_clean1f, 'g', alpha=0.5)

red_patch = ptch.Patch(color='r', label='TX')
blue_patch = ptch.Patch(color='b', label='RX')
green_patch = ptch.Patch(color='g', label='RX Clean')
plt.legend(handles=[red_patch, blue_patch, green_patch])
plt.xlabel('Freq [KHz]')
plt.ylabel('P [dBm]')
plt.title('Single Sine Wave')

plt.show()
