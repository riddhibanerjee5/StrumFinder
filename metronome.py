""" Metronome class used to connect serially to a microcontroller that acts as a metronome.

To connect serially, the data port must be specified. Two ports will be seen when connecting
the microcontroller which is the data port and the REPL port. Trial and error may have to 
be used to see when one is which. For example, if my REPL port is COM6 and my data port is COM3, 
I connect with COM3

set_bpm, play, and pause all send commands to the microcontroller. set_bpm sets the speed of 
the metronome, play starts the metronome, and pause stops the metronome. set_bpm must be 
done before sending play or pause. calculate_bpm is used to calculate the bpm from a song
and is made to be used for set_bpm.
"""

import sys
import serial
import time
from aubio import tempo, source
from scipy.io import wavfile
from numpy import mean, median, diff


class metronome:
    # constructor
    # port and filename are strings, bpm is a float
    # filename and bpm are optional parameters 
    def __init__(self, port=None, filename=None, bpm=-1):
        self.port = port                                        # port to communicate on
        self.serial_connection = serial.Serial(self.port, 115200)    # serial connection to microcontroller
        self.filename = filename                                # file to calculate bpm from
        self.bpm = bpm                                          # current bpm of metronome
        
    # set the metronome speed
    def set_bpm(self, bpm):
        # bpm valid check
        if bpm < 0 or type == str:
            print(bpm)
            print(type(bpm))
            print('Invalid bpm')
            return

        # send the bpm to the metronome to play
        bpm_str = "set {bpm_str:.3f}\r\n".format(bpm_str = bpm)
        input = bytes(bpm_str, encoding='utf-8')
        self.serial_connection.write(input)

    # play the metronome
    def play(self):
        self.serial_connection.write(b'play\r\n')

    # pause the metronome
    def pause(self):
        self.serial_connection.write(b'pause\r\n')

    def unpause(self, bpm, song_time_pos):
        if bpm < 0 or type == str:
            print(bpm)
            print(type(bpm))
            print('Invalid bpm')
            return

        if song_time_pos < 0 or (type(song_time_pos) != float and type(song_time_pos) !=  int):
            print('Invalid time of song')
            return

        mspb = 60.0 / bpm * 1000
        time_to_beat = mspb - (song_time_pos % mspb)
        #print("bpm: ", str(bpm), ", mspb: ", str(mspb), ", song time pause: ", str(song_time_pos), ", time to beat: ", str(time_to_beat))
        input_str = "unpause {}\r\n".format(time_to_beat)
        #print(input_str)
        input = bytes(input_str, encoding='utf-8')
        self.serial_connection.write(input)

    # set the serial connection to the microcontroller
    def set_serial(self, port):
        self.port = port
        self.serial_connection = serial.Serial(port, 115200)

    # calculate bpm from a .wav file
    # filename is an opional parameter, it is only needed
    # if a file was not given when using the constructor
    def calculate_bpm(self, filename=None):
        # set the file to the one in the contructor if given
        if filename != None:
            self.filename = filename

        # check that the file has been input and is a .wav file
        if self.filename == None:
            print("No file specified")
            return -1
        elif self.filename.find('.wav') == -1:
            print("Invalid file. Needs .wav")
            return -1

        win_s = 512                 # fft size
        hop_s = win_s // 2          # hop size

        # open wavfile to get samplerate
        samplerate, tempaudio = wavfile.read(self.filename)

        # get the tempo
        s = source(self.filename, samplerate, hop_s)
        samplerate = s.samplerate
        o = tempo("default", win_s, hop_s, samplerate)

        # tempo detection delay, in samples
        # default to 4 blocks delay to catch up with
        delay = 4. * hop_s

        # list of beats, in samples
        beats = []

        # total number of frames read
        total_frames = 0
        while True:
            samples, read = s()
            is_beat = o(samples)
            if is_beat:
                this_beat = o.get_last_s()
                beats.append(this_beat)
            total_frames += read
            if read < hop_s: break

        # calculate bpm
        bpms = 60./ diff(beats)
        bpm = median(bpms)

        return bpm

