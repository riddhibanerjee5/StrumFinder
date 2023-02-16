import soundfile as sf
import math
from math import log2, pow
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pretty_midi as midi

def strum_direction(magnitude_stft):
    # Calculate the energy of the signal by summing the magnitude of the STFT
    energy = np.sum(magnitude_stft, axis=1)
    
    # Calculate the slope of the energy signal over time
    slope = np.diff(energy)
    
    # Determine the strum direction based on the slope of the energy signal
    if np.mean(slope) > 0:
        return "Up strum"
    else:
        return "Down strum"


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
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

x = midi.PrettyMIDI('faster_strums.mid')

convert = True
if (convert):
    combined = midi.Instrument(program=0)
    for instrument in x.instruments:
        for note in instrument.notes:
            combined.notes.append(note)
    x.instruments = [combined]

i = 0
for instrument in x.instruments:
    print("Instrument", i, instrument.name)
    i += 1
    notes = np.array(instrument.notes)
    indices = np.argsort([note.start for note in notes])
    notes = notes[indices]
    
    chords = np.zeros((2,))
    start = notes[0]
    n = 100
    for i in range(len(notes[0:n])):
        if (notes[i].start - notes[i-1].start > 0.01 and i > 0):
            #print()
            end = notes[i-1]
            chords = np.append(chords, [start,end])
            if (start.pitch < end.pitch):
                print("downstrum\n")
            else:
                print("upstrum\n")
            start = notes[i]
            
        freq = midi.note_number_to_hz(notes[i].pitch)
        print(convertToNote(freq, name), freq, notes[i])

    if (start.pitch < notes[notes.size-1].pitch):
        print("downstrum\n")
    else:
        print("upstrum\n")

    # strum direction
    #for chord in chords:
    #    if (chord[0].pitch < chord[1].pitch):
    #        print("downstrum\n")
    #    else:
    #        print("upstrum\n")


    #if (notes.size > 1):
    #    if (notes[0].pitch < notes[n-1].pitch):
    #        print("downstrum\n")
    #    else:
    #        print("upstrum\n")
