import soundfile as sf
import math
from math import log2, pow
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


def stft(n, t, w, x, M, W, Fs):
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


x = []
file = open("chirp.txt")
while True:
    line = file.readline()
    if not line:
        break
    x.append(float(line))
file.close()

W = 100
Fs = 44100.0
n = []
t = []
w = []

M = math.floor(len(x)/W)

X = stft(n, t, w, x, M, W, Fs)

for i in range(len(X)):
    X[i] = abs(X[i])


def show_graph():
    plt.pcolormesh(X, cmap='inferno')
    plt.colorbar()
    plt.xlabel("Frequency")
    plt.ylabel("Time")
    plt.title("Short Time Fourier Transform")
    plt.show()
