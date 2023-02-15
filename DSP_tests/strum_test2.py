import soundfile as sf
import math
from math import log2, pow
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import librosa

import heapq

def top_ten_greatest(arr):
    # Flatten the 2D array into a 1D array
    flat_arr = [item for sublist in arr for item in sublist]
    # Find the 10 greatest elements using heapq
    top_ten = heapq.nlargest(10, flat_arr)
    return top_ten

def count_greater_than(arr, threshold):
    count = 0
    for sublist in arr:
        for item in sublist:
            if item > threshold:
                count += 1
    return count



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


def graph(X):
    plt.pcolormesh(X, cmap='inferno')
    plt.colorbar()
    plt.xlabel("Frequency")
    plt.ylabel("Time")
    plt.title("Short Time Fourier Transform")
    plt.show()



n = []
t = []
w = []

x, Fs = sf.read("pigsbar.wav")
x = x.transpose()
M = math.floor(len(x[0])/100)
W = math.floor(len(x[0])/M)

X = stft(n, t, w, x[0], M, W, Fs)

# find max frequencies
for i in range(len(X)):
    X[i] = abs(X[i])
freqs = findMaxFreq(X, Fs)


X = np.array(X)
A = np.flip(X,0)
#graph(X)

magnitude = X[:,1:50]

# Get the onset frames
onset_frames = librosa.onset.onset_detect(y=x[0], sr=44100, backtrack=False)

for onset_frame in onset_frames:
    # Compute the slope of the energy in the time-frequency plane for the frame index
    frame_magnitude = magnitude[onset_frame, :]
    #freq, time = np.meshgrid(np.arange(frame_magnitude.shape[0]), np.arange(frame_magnitude.shape[1]))
    freq = np.array(np.meshgrid(np.arange(frame_magnitude.shape[0])))
    time = np.array([onset_frame])
    slope = np.polyfit(time.ravel(), freq.ravel(), 1, w=frame_magnitude.ravel())[0]

    # Check the slope to determine if the signal is being upstrummed or downstrummed
    if slope > 0:
        print("Strum direction: Up")
    else:
        print("Strum direction: Down")





#print(top_ten_greatest(X))
#print(count_greater_than(X, 10))

f = False
strums = t
for i in range(len(strums)):
    strums[i] = 0

for i in range(len(X)):
    for j in range(len(X[i][1:50])):
        if f == False and X[i][j] > 3:
            f = True
            index = j
            break
        elif f == True and X[i][index+1] > 3:
            f = True
            strums[i-1] = 1

file = open("strums.txt", 'w')
file.write("Time of Downstrums\n")
file.write("\n")
for i in range(len(t)):
    if strums[i] == 1:
        file.write(str(t[i]))
        file.write("\n")
file.close()

#how can I find if a guitar is being upstrummed or downstrummed using the short time fourier transform of a guitar signal
#I have completed the STFT, can you write some Python code that implements the analysis of the slope of the energy in the time-frequency plane?