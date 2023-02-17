from math import log2, pow
import numpy as np
import pretty_midi as midi


class Chord():
    def __init__(self, start, strum):
        self.start = start
        self.strum = strum


def convertToNote(f, name):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    h = round(12*log2(f/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


def generateStrums(filename):
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    x = midi.PrettyMIDI(filename)
    chords = np.array([])

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
        
        start = notes[0]
        n = notes.size
        for i in range(len(notes[0:n])):
            if (notes[i].start - notes[i-1].start > 0.01 and i > 0):
                end = notes[i-1]
                if (start.pitch < end.pitch):
                    print("downstrum\n")
                    chords = np.append(chords, Chord(start.start,False))
                else:
                    print("upstrum\n")
                    chords = np.append(chords, Chord(start.start,True))
                start = notes[i]
                
            freq = midi.note_number_to_hz(notes[i].pitch)
            print(convertToNote(freq, name), freq, notes[i])

        if (start.pitch < notes[n-1].pitch):
            print("downstrum\n")
            chords = np.append(chords, Chord(start.start,False))
        else:
            print("upstrum\n")
            chords = np.append(chords, Chord(start.start,True))

    return chords