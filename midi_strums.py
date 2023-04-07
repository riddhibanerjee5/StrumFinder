from math import log2, pow
import numpy as np
import pretty_midi as midi
import sys
from aubio import source, notes
from mido import Message, MetaMessage, MidiFile, MidiTrack, second2tick, bpm2tempo
from scipy.io import wavfile


class Chord():
    def __init__(self, start, strum, notes):
        self.start = start
        self.strum = strum
        self.notes = notes
        self.chord_name = ""

    def determineChord(self, chord):
        chordName = ""
        name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        name = np.array(name)

        if (chord.strum == False):
            notes = chord.notes
        else:
            notes = np.flip(chord.notes)

        # get names of notes in chord
        names = np.array([])
        for note in notes:
            freq = midi.note_number_to_hz(note.pitch)
            #chordName = chordName + convertToNote2(freq,name)
            names = np.append(names, convertToNote2(freq,name))
        
        # get unique notes
        _, indices = np.unique(names, return_index=True)
        names = names[np.sort(indices)]
        chordName = names[0]

        # reorder note name array to begin at root note
        start = np.where(name == names[0])[0][0]
        tmp = np.concatenate((name[start:], name[:start]))

        # get intervals
        intervals = np.array([])
        for i in names:
            intervals = np.append(intervals, np.where(tmp == i)[0][0])
        intervals = np.sort(intervals)

        # determine chord
        #diads
        if (len(intervals)==2):
            if (intervals[1]==1):
                chordName = chordName + "b2 diad"
            elif (intervals[1]==2):
                chordName = chordName + "2 diad"
            elif (intervals[1]==3):
                chordName = chordName + "b3 diad"
            elif (intervals[1]==4):
                chordName = chordName + "3 diad"
            elif (intervals[1]==5):
                chordName = chordName + "4 diad"
            elif (intervals[1]==6):
                chordName = chordName + "b5 diad"
            elif (intervals[1]==7):
                chordName = chordName + "5 diad"
            elif (intervals[1]==8):
                chordName = chordName + "b6 diad"
            elif (intervals[1]==9):
                chordName = chordName + "6 diad"
            elif (intervals[1]==10):
                chordName = chordName + "b7 diad"
            elif (intervals[1]==11):
                chordName = chordName + "7 diad"
        #triads
        elif (len(intervals)==3):
            if (intervals[1]==4 and intervals[2] == 7):
                chordName = chordName + " major"
            elif (intervals[1]==3 and intervals[2] == 7):
                chordName = chordName + " minor"
            elif (intervals[1]==2 and intervals[2]==7):
                chordName = chordName + "sus2"
            elif (intervals[1]==5 and intervals[2]==7):
                chordName = chordName + "sus4"
            elif (intervals[1]==3 and intervals[2]==6):
                chordName = chordName + " dim"
            elif (intervals[1]==4 and intervals[2]==8):
                chordName = chordName + " aug"
            else:
                chordName = ""
                for i in names:
                    chordName += i
        # four notes
        elif (len(intervals)==4):
            if (intervals[1]==4 and intervals[2] == 7 and intervals[3]==10):
                chordName = chordName + "7 (dom7)"
            elif (intervals[1]==3 and intervals[2] == 7 and intervals[3]==10):
                chordName = chordName + "m7"
            elif (intervals[1]==4 and intervals[2] == 7 and intervals[3]==11):
                chordName = chordName + "maj7"
            elif (intervals[1]==3 and intervals[2] == 6 and intervals[3]==9):
                chordName = chordName + "dim7"
            else:
                chordName = ""
                for i in names:
                    chordName += i

        self.chord_name = chordName
        return chordName


def convertToNote(f, name):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    h = round(12*log2(f/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

def convertToNote2(f, name):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    h = round(12*log2(f/C0))
    n = h % 12
    return name[n]


def getMidiBpm(filename):
    x = midi.PrettyMIDI(filename)
    return x.estimate_tempo()


def generateStrums(filename, combine):
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    name = np.array(name)

    x = midi.PrettyMIDI(filename)
    chords = np.array([])

    # combine all midi instruments?
    if (combine):
        combined = midi.Instrument(program=0)
        for instrument in x.instruments:
            for note in instrument.notes:
                combined.notes.append(note)
        x.instruments = [combined]

    for instrument in x.instruments:
        notes = np.array(instrument.notes)
        indices = np.argsort([note.start for note in notes])
        notes = notes[indices]
        
        start = notes[0]
        start_index = 0
        n = notes.size
        for i in range(len(notes[0:n])):
            if (notes[i].start - notes[i-1].start > 0.1 and i > 0):
                end = notes[i-1]
                end_index = i-1
                chordNotes = notes[start_index:end_index+1]
                if (start.pitch < end.pitch):
                    chord = Chord(start.start,False,chordNotes)
                    chord.determineChord(chord)
                    chords = np.append(chords, chord)
                else:
                    chord = Chord(start.start,True,chordNotes)
                    chord.determineChord(chord)
                    chords = np.append(chords, chord)
                start = notes[i]
                start_index = i

        chordNotes = notes[start_index:n]
        if (start.pitch < notes[n-1].pitch):
            chord = Chord(start.start,False,chordNotes)
            chord.determineChord(chord)
            chords = np.append(chords, chord)
        else:
            chord = Chord(start.start,True,chordNotes)
            chord.determineChord(chord)
            chords = np.append(chords, chord)

    return chords