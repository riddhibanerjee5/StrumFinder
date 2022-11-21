#! /usr/bin/env python
import soundfile as sf
#import aubio as ab
from aubio import pitch
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

n = []
t = []
w = []

x, Fs = sf.read('smiles.wav')
x = x.transpose()
# total sixteenth notes (time divisions) = length*bps*16
bps = 85.0/60.0                  # beats per second 139
length = len(x[1])/Fs             # length in seconds
M = math.floor(length*bps*16.0)   # sixteenth notes
W = math.floor(len(x[1])/M)

X = stft(n,t,w,x[1],M,W,Fs)

p = pitch("yin",W,M,Fs)
p.set_unit("midi")





plt.pcolormesh(X,cmap='inferno')
plt.colorbar()
plt.xlabel("Frequency")
plt.ylabel("Time")
plt.title("Short Time Fourier Transform")
plt.show()