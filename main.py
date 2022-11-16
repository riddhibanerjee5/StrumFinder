from playsound import playsound
from tkinter import *
import multiprocessing
from tkinter import filedialog


root = Tk()
root.title('Strum Finder')  # giving the title for our window
root.geometry("1000x1000")


def openFile():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("wav files",
                                                      "*.wav*"),

                                                     ))


def play():
    # playsound('1.mp3')
    playsound('2.wav')


# title on the screen you can modify it
title = Label(root, text="Strum Finder", bd=9, relief=GROOVE,
              font=("times new roman", 50, "bold"), bg="white", fg="blue")
title.pack(side=TOP, fill=X)

select_file_button = Button(root, text="Select File", font=(
    "Helvetica", 16), relief=GROOVE, command=openFile)
select_file_button.pack(pady=40)

# making a button which trigger the function so sound can be played
play_button = Button(root, text="Play Song", font=(
    "Helvetica", 16), relief=GROOVE, command=play)
play_button.pack(pady=40)

stop_button = Button(root, text="Stop Song", font=(
    "Helvetica", 16), relief=GROOVE,)
stop_button.pack(pady=40)

root.mainloop()
