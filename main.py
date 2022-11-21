from playsound import playsound
from tkinter import *
import multiprocessing
from tkinter import filedialog
from PIL import ImageTk, Image
import pygame

pygame.mixer.init()

# testing

root = Tk()
root.title('Strum Finder')
root.geometry("1000x1000")
root.configure(bg="light blue")

############ Images ################
frame = Frame(root, width=200, height=200)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

sound_wave_img = ImageTk.PhotoImage(Image.open("sound_wave.jfif"))

label = Label(frame, image=sound_wave_img)
label.pack()

####################################


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


# title on the screen you can modify it
title = Label(root, text="Strum Finder", bd=9, relief=GROOVE,
              font=("times new roman", 50, "bold"), bg="light blue", fg="blue")
title.pack(side=TOP, fill=X)

select_file_button = Button(root, text="Select File", font=(
    "Helvetica", 16), relief=GROOVE, command=openFile, bg="magenta")
select_file_button.place(y=175, x=100)

# making a button which trigger the function so sound can be played
play_button = Button(root, text="Play Song", font=(
    "Helvetica", 16), relief=GROOVE, command=play, bg="green")
play_button.place(y=175, x=700)

stop_button = Button(root, text="Stop Song", font=(
    "Helvetica", 16), relief=GROOVE, command=stop, bg="red")
stop_button.place(y=175, x=1300)

root.mainloop()
