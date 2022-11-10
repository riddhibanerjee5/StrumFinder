import soundfile as sf
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


def stft(n, t, w, x, W, Fs):
    M = math.floor(len(x) / W)
    X = []
    for i in range(M):
        n.append(i*W)
        t.append(n[i]/Fs)
        y = x[i*W:(i+1)*W]
        X.append(np.fft.fft(y))
    for i in range(W):
        w.append((2*math.pi*i)/float(W))
    return X

def result():
    for i in range(len(X)):
        for j in range(len(X[i])):
            if (abs(X[i][j]) < 0.0000001):
                X[i][j] = 0
            print("X[", i, "][", j, "]: ", X[i][j])

W = 5000
Fs = 44100.0
n = []
t = []
w = []

#x =  [0.00, 0.59, 0.95, 0.95, 0.59, 0.00, -0.59, -0.95, -0.95, -0.59, 0.00, 0.95, 0.59, -0.59, -0.95, 0.00, 0.95, 0.59, -0.59, -0.95, 0.00, 0.95, -0.59, -0.59, 0.95, 0.00, -0.95, 0.59, 0.59, -0.95, 0.00, 0.59, -0.95, 0.95, -0.59, 0.00, 0.59, -0.95, 0.95, -0.59, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.59, 0.95, -0.95, 0.59, 0.00, -0.59, 0.95, -0.95, 0.59, 0.00, -0.95, 0.59, 0.59, -0.95, 0.00, 0.95, -0.59, -0.59, 0.95, 0.00, -0.95, -0.59, 0.59, 0.95, 0.00, -0.95, -0.59, 0.59, 0.95, 0.00, -0.59, -0.95, -0.95, -0.59, 0.00, 0.59, 0.95, 0.95, 0.59, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

#file = open("chirp.txt")
#while True:
#    line = file.readline()
#    if not line:
#        break
#    x.append(float(line))
#file.close()

x, Fs = sf.read('gods.wav')
x = x.transpose()

X = stft(n,t,w,x[1],W,Fs)

for i in range(len(X)):
    X[i]=abs(X[i])
plt.pcolormesh(X,cmap='inferno')
plt.colorbar()
plt.xlabel("Frequency")
plt.ylabel("Time")
plt.title("Short Time Fourier Transform")
plt.show()