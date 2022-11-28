from playsound import playsound
from os import startfile
from tkinter import *
import multiprocessing
from tkinter import filedialog
from PIL import ImageTk, Image
import pygame
from stft_chirp import show_graph
from stft import generateNotes
pygame.mixer.init()

root = Tk()
root.title('Strum Finder')
root.geometry("1000x1000")
root.configure(bg="light blue")

title = Label(root, text="Strum Finder", bd=9, relief=GROOVE,
              font=("times new roman", 50, "bold"), bg="light blue", fg="blue")
title.pack(side=TOP, fill=X)

############################### Images ################################
frame = Frame(root, width=50, height=50)
frame.pack()
#frame.place(anchor='center', relx=0.5, rely=0.5)
frame.place(y=500, x=620)

sound_wave_img = ImageTk.PhotoImage(Image.open("sound_wave.jfif"))

label = Label(frame, image=sound_wave_img)
label.pack()
#######################################################################


############################## FUNCTIONS ########################################
def openFile():
    global soundFile
    soundFile = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("wav files",
                                                      "*.wav*"),
                                                      ))


def play():
    if soundFile:
        playSound = pygame.mixer.Sound(soundFile)
        playSound.play(0, 5000)


def stop():
    pygame.mixer.pause()


def openNotes():
    generateNotes(soundFile)
    startfile("notes.txt")
##################################################################################


##################### ORIGINAL SONG ####################################
original_song_label = Label(root, text="Original Song: ", font=(
    "Helvetica", 25, "bold"), bg="light blue")
original_song_label.place(y=120, x=90)

select_file_button = Button(root, text="Select File", font=(
    "Helvetica", 16), relief=GROOVE, command=openFile, bg="magenta")
select_file_button.place(y=200, x=100)

# making a button which trigger the function so sound can be played
play_button = Button(root, text="Play Song", font=(
    "Helvetica", 16), relief=GROOVE, command=play, bg="green")
play_button.place(y=200, x=700)

stop_button = Button(root, text="Stop Song", font=(
    "Helvetica", 16), relief=GROOVE, command=stop, bg="red")
stop_button.place(y=200, x=1300)
#########################################################################


###################### GENERATING STRUM PATTERNS ########################
strum_pattern_label = Label(root, text="Strum Pattern: ", font=(
    "Helvetica", 25, "bold"), bg="light blue")
strum_pattern_label.place(y=300, x=90)

# TO DO: Add functionality on press
generate_patterns_button = Button(root, text="Generate Strum Patterns", font=(
    "Helvetica", 16), relief=GROOVE, bg="yellow")
generate_patterns_button.place(y=380, x=100)

generate_patterns_button = Button(root, text="Generate Notes", font=(
    "Helvetica", 16), relief=GROOVE, command=openNotes, bg="yellow")
generate_patterns_button.place(y=480, x=100)

# TO DO: Add functionality on press
start_button = Button(root, text="Start", font=(
    "Helvetica", 16), relief=GROOVE, bg="yellow")
start_button.place(y=380, x=720)

show_graph_button = Button(root, text="Show Plot", font=(
    "Helvetica", 16), relief=GROOVE, command=show_graph, bg="yellow")
show_graph_button.place(y=380, x=1300)

#########################################################################

root.mainloop()
