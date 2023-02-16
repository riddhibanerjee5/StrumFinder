from math import log2, pow
import numpy as np
import pretty_midi as midi


def convertToNote(f, name):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    h = round(12*log2(f/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


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
