import numpy as np
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

x, Fs = sf.read("pigstrum.wav")
x = x.transpose()
M = math.floor(len(x[0])/100)
W = math.floor(len(x[0])/M)

X = stft(n, t, w, x[0], M, W, Fs)

# find max frequencies
for i in range(len(X)):
    X[i] = abs(X[i])

X = np.array(X)
A = np.flip(X,0)
graph(X)

magnitude = X
threshold = .5

# Assume that `magnitude` is a 2D Numpy array representing the magnitude of the STFT
# of the guitar signal, with dimensions (num_frequencies, num_time_frames)

# Extract the indices of the onset frames, where an onset is defined as a sudden change
# in the magnitude of the signal
onset_frames = np.where(np.diff(np.max(magnitude, axis=0)) > threshold)[0]

strum_directions = []

for onset_frame in onset_frames:
    # Compute the slope of the energy in the time-frequency plane for the frame index
    frame_magnitude = magnitude[:, onset_frame]
    time = np.array([onset_frame])
    freq = np.arange(frame_magnitude.shape[0])
    slope = np.polyfit(time.ravel(), freq.ravel(), 1, w=frame_magnitude.ravel())[0]

    # Check the slope to determine if the signal is being upstrummed or downstrummed
    if slope > 0:
        strum_directions.append("Up")
    else:
        strum_directions.append("Down")

print("Strum directions: ", strum_directions)
