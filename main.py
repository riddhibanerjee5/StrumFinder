from metronome import metronome
from playsound import playsound
from os import startfile
from tkinter import *
import multiprocessing
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image
from pygame import mixer
from stft_chirp import show_graph
from stft import generateNotes
mixer.init()

colors = {"turqoise": "#55D6BE",
          "magicMint": "#ACFCD9",
          "royalPurple": "#7D5BA6",
          "gainsboro": "#DDDDDD",
          "fieryRose": "#FC6471",
          "orangeSoda": "#F95738",
          "plumWeb": "#F9B9F2",
          "snow": "snow",
          "white": "white",
          "mediumSlateBlue": "#736CED",
          "languidLavender": "#E5D4ED",
          "mustard": "#FFD449", }

root = Tk()
root.title('Strum Finder')
root.geometry("1000x1000")
root.configure(bg=colors["white"])

title = Label(root, text="Strum Finder", bd=9, relief=GROOVE,
              font=("Helvetica", 50, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
title.pack(side=TOP, fill=X)

metro = metronome()
pauseFlag = 0
metroOnFlag = 0

############################### Images ################################
#frame = Frame(root, width=50, height=50)
# frame.pack()
#frame.place(anchor='center', relx=0.5, rely=0.5)
#frame.place(y=500, x=620)

#sound_wave_img = ImageTk.PhotoImage(Image.open("sound_wave.jfif"))

#label = Label(frame, image=sound_wave_img)
# label.pack()
#######################################################################


############################## FUNCTIONS ########################################

def openFile():
    global soundFile
    global playSound
    soundFile = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("wav files",
                                                      "*.wav*"),
                                                      ))
    playSound = mixer.music.load(soundFile)


def play():
    global pauseFlag
    global metroOnFlag
    if soundFile:
        if pauseFlag == 1:
            songTime = mixer.music.get_pos()

            if metroOnFlag and metro != None:
                metro.unpause(metro.calculate_bpm(soundFile), songTime)

            mixer.music.unpause()
        else:
            mixer.music.play()

            if metroOnFlag and metro != None:
                metro.set_bpm(metro.calculate_bpm(soundFile))
                metro.play()

def pause():
    global pauseFlag
    global metroOnFlag

    mixer.music.pause()

    if metroOnFlag and metro != None:
        metro.pause()

    pauseFlag = 1

def restart():
    global pauseFlag
    global metroOnFlag

    if soundFile:
        mixer.music.stop()
        pauseFlag = 0

    if metroOnFlag and metro != None:
        metro.pause()

def openNotes():
    generateNotes(soundFile)
    startfile("notes.txt")


def serial():
    global metroOnFlag
    port = simpledialog.askstring(title="Select Port",
                                  prompt="Port:")
    metro.set_serial(port)
    metroOnFlag = 1 


def start_metronome():
    global metroOnFlag

    metroOnFlag = 1

    if metro != None:
        metro.set_bpm(metro.calculate_bpm(soundFile))
        metro.play()


def pause_metronome():
    if metro != None:
        metro.pause()


##################################################################################
##################### ORIGINAL SONG ####################################
button_width_apart = 400

original_song_label = Label(root, text="Original Song", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
original_song_label.place(y=120, x=650)     # x = 90 before

select_file_button = Button(root, text="Select File", font=(
    "Helvetica", 16), relief=GROOVE, command=openFile, bg=colors["magicMint"])
select_file_button.place(y=200, x=100)

# making a button which trigger the function so sound can be played
play_button = Button(root, text="Play Song", font=(
    "Helvetica", 16), relief=GROOVE, command=play, bg=colors["magicMint"])
play_button.place(y=200, x=100+button_width_apart)

stop_button = Button(root, text="Pause Song", font=(
    "Helvetica", 16), relief=GROOVE, command=pause, bg=colors["magicMint"])
stop_button.place(y=200, x=100+(2*button_width_apart))

restart_button = Button(root, text="Restart Song", font=(
    "Helvetica", 16), relief=GROOVE, command=restart, bg=colors["magicMint"])
restart_button.place(y=200, x=100+(3*button_width_apart))

#########################################################################


###################### GENERATING STRUM PATTERNS ########################
strum_pattern_label = Label(root, text="Strum Pattern", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
strum_pattern_label.place(y=300, x=650)

# TO DO: Add functionality on press
generate_patterns_button = Button(root, text="Generate Strum Patterns", font=(
    "Helvetica", 16), relief=GROOVE, bg=colors["languidLavender"])
generate_patterns_button.place(y=380, x=100)

generate_patterns_button = Button(root, text="Generate Notes", font=(
    "Helvetica", 16), relief=GROOVE, command=openNotes, bg=colors["languidLavender"])
generate_patterns_button.place(y=480, x=670)

# TO DO: Add functionality on press
start_button = Button(root, text="Start", font=(
    "Helvetica", 16), relief=GROOVE, bg=colors["languidLavender"])
start_button.place(y=380, x=720)

show_graph_button = Button(root, text="Show Plot", font=(
    "Helvetica", 16), relief=GROOVE, command=show_graph, bg=colors["languidLavender"])
show_graph_button.place(y=380, x=1300)

#########################################################################


######################### METRONOME #####################################
metronome_label = Label(root, text="Metronome", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
metronome_label.place(y=600, x=670)

select_serial_port_button = Button(root, text="Select Port", font=(
    "Helvetica", 16), relief=GROOVE, command=serial, bg=colors["mustard"])
select_serial_port_button.place(y=675, x=100)

start_metronome_button = Button(root, text="Start", font=(
    "Helvetica", 16), relief=GROOVE, command=start_metronome, bg=colors["mustard"])
start_metronome_button.place(y=675, x=720)

stop_metronome_button = Button(root, text="Stop", font=(
    "Helvetica", 16), relief=GROOVE, command=pause_metronome, bg=colors["mustard"])
stop_metronome_button.place(y=675, x=1320)
#########################################################################

root.mainloop()
