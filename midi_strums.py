from math import log2, pow
import numpy as np
import pretty_midi as midi
import sys
from aubio import source, notes
from mido import Message, MetaMessage, MidiFile, MidiTrack, second2tick, bpm2tempo
from scipy.io import wavfile


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


    
def wav_to_midi(wavFile, midiFile):
    filename = wavFile
    midioutput = midiFile

    downsample = 1
    samplerate = 44100 // downsample
    samplerate, tempaudio = wavfile.read(filename)

    win_s = 512 // downsample # fft size
    hop_s = 256 // downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    notes_o = notes("default", win_s, hop_s, samplerate)

    print("%8s" % "time","[ start","vel","last ]")

    # create a midi file
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    ticks_per_beat = mid.ticks_per_beat # default: 480
    bpm = 120 # default midi tempo

    tempo = bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))

    def frames2tick(frames, samplerate=samplerate):
        sec = frames / float(samplerate)
        return int(second2tick(sec, ticks_per_beat, tempo))

    last_time = 0

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        new_note = notes_o(samples)
        if (new_note[0] != 0):
            note_str = ' '.join(["%.2f" % i for i in new_note])
            print("%.6f" % (total_frames/float(samplerate)), new_note)
            delta = frames2tick(total_frames) - last_time
            if new_note[2] > 0:
                track.append(Message('note_off', note=int(new_note[2]),
                    velocity=127, time=delta)
                    )
            track.append(Message('note_on',
                note=int(new_note[0]),
                velocity=int(new_note[1]),
                time=delta)
                )
            last_time = frames2tick(total_frames)
        total_frames += read
        if read < hop_s: break

    mid.save(midioutput)

wav_to_midi('wav-files/riptide_acoustic.wav', 'wav-files/riptide_acoustic.mid')

