import scipy.io as sp
import numpy as np
import matplotlib.pyplot as plt

# fh = open("/home/wimnet/Desktop/tranceler_mt_rt_final_works/build/tx_file", "rb")
# fh = open("/home/wimnet/Desktop/tranceler_mt_rt_final_works/build/rx_file", "rb")
fh = open("/home/wimnet/Desktop/tranceler_mt_rt_final_works/build/y_clean_file", "rb")
y =np.fromfile(fh, dtype=float)
# print (y.shape)

x = np.arange(y.shape[0])
# print (x.shape)

size = 2000
y1 = y[0:size]
x1 = x[0:size]

plt.plot(x1,y1)

plt.show()