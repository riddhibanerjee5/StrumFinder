import time
import board
import sys
import usb_cdc
import pwmio

# starting variables
serial = usb_cdc.data       # allow for serial connection
input_byte = None           # input from serial connection
play_flag = 0               # flag for if the piezo should play or not
piezo = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=440, variable_frequency=True)   # create a metronome with pwm
piezo.frequency = 440       # tone of the metronome noise
bps = None                  # beats per second
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
            bps = 60.0 / bpm
        # play the metronome
        elif input.find('play') != -1:
            play_flag = 1
        # pause the metronome
        elif input.find('pause') != -1:
            play_flag = 0

    # play the metronome while the play_flag is true
    while play_flag:
        if serial.in_waiting > 0:
            break
        
        # tick cycle
        piezo.duty_cycle = 65535 // 2  # On 50%
        time.sleep(beep_len)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(bps-beep_len)  # Pause between notes


    