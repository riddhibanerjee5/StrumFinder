import sys
import serial
import time
from aubio import tempo, source
from scipy.io import wavfile
from numpy import mean, median, diff


class metronome:
    # constructor
    def __init__(self, port, filename=None, bpm=None):
        self.port = port                                        # port to communicate on
        self.serial_connection = serial.Serial(port, 115200)    # serial connection to microcontroller
        self.filename = filename                                # file to calculate bpm from
        self.bpm = bpm                                          # current bpm of metronome
        
    # set the metronome speed
    def set_metronome(self, bpm):
        # bpm valid check
        if bpm < 0:
            print('Invalid bpm')
            return

        # send the bpm to the metronome to play
        bpm_str = "set {bpm_str:.3f}\r\n".format(bpm_str = bpm)
        input = bytes(bpm_str, encoding='utf-8')
        self.serial_connection.write(input)

    # play the metronome
    def play_metronome(self):
        self.serial_connection.write(b'play\r\n')

    # pause the metronome
    def pause_metronome(self):
        self.serial_connection.write(b'pause\r\n')

    # set the serial connection to the microcontroller
    def set_serial(self, port):
        self.serial_connection = serial.Serial(port, 115200)

    # calculate bpm from a .wav file
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

