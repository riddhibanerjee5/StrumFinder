import soundfile as sf
import math
from math import log2, pow
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from scipy.signal import butter, lfilter


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


def findMaxFreq(X, Fs):
    freqs = []
    for i in range(len(X)):
        Xmax = 0.0
        fmax = 0.0
        for j in range(len(X[i])):
            if X[i][j] > Xmax:
                Xmax = X[i][j]
                if ((j*Fs)/len(X[i])) < (Fs/2) and (j*Fs)/len(X[i]) > 0:
                    fmax = (j*Fs)/len(X[i])
        freqs.append(fmax)
    return freqs


def findF0(X, Fs):
    freqs = []
    for i in range(len(X)):
        Xmax = 0.0
        freqs.append([])
        for j in range(len(X[i])):
            if X[i][j] > 40 and ((j*Fs)/len(X[i])) < (Fs/2) and (j*Fs)/len(X[i]) > 0:
                freqs[i].append((j*Fs)/len(X[i]))
        #freqs.append(fmax)
    return freqs


def convertToNote(f, name):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    h = round(12*log2(f/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


def result(X):
    for i in range(len(X)):
        for j in range(len(X[i])):
            if (abs(X[i][j]) < 0.0000001):
                X[i][j] = 0
            print("X[", i, "][", j, "]: ", X[i][j])


n = []
t = []
w = []

x, Fs = sf.read("pigstrum.wav")
x = x.transpose()
# total sixteenth notes (time divisions) = length*bps*16
bps = 85.0/60.0                  # beats per second (139 gods) (85 smiles) (85 priestess)
length = len(x[0])/Fs             # length in seconds
M = math.floor(length*bps*4.0)   # sixteenth notes
W = math.floor(len(x[0])/M)

X = stft(n, t, w, x[0], M, W, Fs)
for i in range(len(X)):
    X[i] = abs(X[i])

# apply filter
X = np.array(X)
passband = [50,650]
order = 5
nyquist_freq = .5 * Fs
low = passband[0] / nyquist_freq
high = passband[1] / nyquist_freq
b, a = butter(order, [low,high], btype='band')
X = lfilter(b, a, X)

# find max frequencies, f0
freq = findMaxFreq(X,Fs)
freqs = findF0(X, Fs)

n = 1
print(t[n])
print(freq[n])
print("")
for i in range(len(freqs[n])):
    print(freqs[n][i])

# convert frequencies to notes (pitch)
A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notes = []
for i in range(len(freqs[n])):
    if freqs[n][i] > 0:
        print(convertToNote(freqs[n][i], name))