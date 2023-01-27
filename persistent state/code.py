""" Metronome microcontroller using a serial connection to receive commands. 

Commands are: play, pause, and set
play starts the metronome
pause stops the metronome
set sets the metronome to a specified bpm

The serial uses both the REPL port and a different port for data. The print
commands are used as debugging statements and show up in the REPL port."""

import time
import board
import sys
import usb_cdc
import pwmio

# starting variables
serial = usb_cdc.data       # allow for serial connection
input_byte = None           # input from serial connection
play_flag = 0               # flag for if the piezo should play or not
unpause_flag = 0
set_flag = 0                # flag for if the metronome has been set
piezo = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=440, variable_frequency=True)   # create a metronome with pwm
piezo.frequency = 440       # tone of the metronome noise
spb = -1                  # beats per second
beep_len = 0.1              # metronome tick length

while (True):
    # read any messages waiting in the buffer
    if serial.in_waiting > 0:
        input_byte = serial.readline()
        
    # interpret serial input
    if (input_byte != None):
        input = input_byte.decode("utf-8") 
        input_byte = None

        # set the bpm of the metronome
        if input.find('set') != -1:
            space = input.find(' ')
            bpm = float(input[space+1:])
            spb = 60.0 / bpm
            print("Set to ", bpm, " beats per minute")
        # unpause from a point in time from the next beat
        elif input.find('unpause') != -1:
            space = input.find(' ')
            time_to_beat_ms = float(input[space+1:])
            time_to_beat = time_to_beat_ms / 1000
            print("Unpaused. Time to next beat: ", time_to_beat, "s")

            # play the metronome but also denote that there is some time to wait for the next beat
            play_flag = 1
            unpause_flag = 1
        # play the metronome
        elif input.find('play') != -1:
            # make sure a bpm has been denoted
            if spb == -1:
                print("BPM has not been set yet, not able to play")
                play_flag = 0
            # play the metronome
            else:
                print("Playing at ", bpm)
                play_flag = 1
        # pause the metronome
        elif input.find('pause') != -1:
            print("Pausing")
            play_flag = 0
        # the metronome will do an upstrum or downstrum
        elif input.find('strum') != -1:
            # play upstrum
            if input.find("up") != -1:
                piezo.frequency = 262
                piezo.duty_cycle = 65535
                time.sleep(beep_len)
                piezo.duty_cycle = 0

                print("Upstrum")
            # play downstrum
            elif input.find("down") != -1:
                piezo.frequency = 440 
                piezo.duty_cycle = 65535 // 2
                time.sleep(beep_len)
                piezo.duty_cycle = 0

                print("Downstrum")

            # reset metronome
            piezo.frequency = 440 
            play_flag = 0

    # play the metronome while the play_flag is true
    while play_flag:
        if serial.in_waiting > 0:
            break
        
        if unpause_flag:
            time.sleep(time_to_beat)
            unpause_flag = 0
            continue

        # tick cycle
        piezo.duty_cycle = 65535 // 2  # On 50%
        time.sleep(beep_len) # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(spb-beep_len)  # Pause between notes
