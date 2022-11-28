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


def generateNotes(file):
    n = []
    t = []
    w = []

    x, Fs = sf.read(file)
    x = x.transpose()
    # total sixteenth notes (time divisions) = length*bps*16
    bps = 85.0/60.0                  # beats per second (139 gods) (85 smiles) (85 priestess)
    length = len(x[0])/Fs             # length in seconds
    M = math.floor(length*bps*4.0)   # sixteenth notes
    W = math.floor(len(x[0])/M)

    X = stft(n, t, w, x[0], M, W, Fs)

    # find max frequencies
    for i in range(len(X)):
        X[i] = abs(X[i])
    freqs = findMaxFreq(X, Fs)

    # convert frequencies to notes (pitch)
    A4 = 440
    C0 = A4*pow(2, -4.75)
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    notes = []
    for i in range(len(freqs)):
        if freqs[i] > 0:
            notes.append(convertToNote(freqs[i], name))
        else:
            notes.append("N/A")

    file = open("notes.txt", 'w')
    file.write("Time                        Note\n")
    file.write("\n")
    for i in range(len(notes)):
        file.write(str(t[i]))
        file.write("            ")
        file.write(notes[i])
        file.write("\n")
    file.close()


def graph(X):
    plt.pcolormesh(X, cmap='inferno')
    plt.colorbar()
    plt.xlabel("Frequency")
    plt.ylabel("Time")
    plt.title("Short Time Fourier Transform")
    plt.show()
