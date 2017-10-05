import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import scipy.fftpack as fft
import os
import sys

# print (sys.argv)
file = ['tx_out', 'sine_wave_2M']
dir_path = os.path.dirname(os.path.realpath(__file__))


fh = open(dir_path + "/" + file[0], "rb")
tx = np.fromfile(fh, dtype=float)

fh = open(dir_path + "/" + file[1], "rb")
rx = np.fromfile(fh, dtype=float)

x = np.arange(tx.shape[0])
# print (x.shape)

step = 4
g = 1
start = 20440 *step
stop = start + int(20440 / g)
# start = 34000
# stop = 37000
# start = 40000
# stop = 60000


x1 = x[start:stop]
tx1 = tx[start:stop]
rx1 = rx[start:stop]


tx1f = fft.fft(tx1)
rx1f = fft.fft(rx1)

bw = 5 * 10 ** 5
step = 2 * bw / tx1f.shape[0]
x1f = np.arange(- bw, bw, step)

# print (tx1f.shape, rx1f.shape, rx_clean1f.shape, x1f.shape)

plt.figure(1)
plt.plot(x1, tx1, 'r', x1, rx1, 'b', alpha=0.5)

red_patch = ptch.Patch(color='r', label='TX')
blue_patch = ptch.Patch(color='b', label='RX')
plt.legend(handles=[red_patch, blue_patch])

p_scale = 1
plt.figure(2)
plt.plot(x1f, p_scale * np.log10(tx1f), 'r', x1f, p_scale * np.log10(rx1f), 'b', alpha=0.5)

red_patch = ptch.Patch(color='r', label='TX')
blue_patch = ptch.Patch(color='b', label='RX')
plt.legend(handles=[red_patch, blue_patch])


plt.show()
