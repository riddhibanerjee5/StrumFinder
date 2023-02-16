import time
from metronome import metronome
from playsound import playsound
from os import startfile
from tkinter import *
import multiprocessing
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image
from pygame import mixer
#from stft_chirp import show_graph
#from stft import generateNotes
from strum import generate_strums
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

# canvas = Canvas(root, width=700, height=100, bg=colors["white"])            # Canvas for strum patterns
# canvas.place(y=450,x=500)

title = Label(root, text="Strum Finder", bd=9, relief=GROOVE,
              font=("Helvetica", 50, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
title.pack(side=TOP, fill=X)

metro = metronome()
pauseFlag = 0
metroOnFlag = 0
metroStrumFlag = 0
playFlag = 0
metroInit = 0

############################### Images ################################
#frame = Frame(root, width=50, height=50)
# frame.pack()
#frame.place(anchor='center', relx=0.5, rely=0.5)
#frame.place(y=500, x=620)

#sound_wave_img = ImageTk.PhotoImage(Image.open("sound_wave.jfif"))

#label = Label(frame, image=sound_wave_img)
# label.pack()

upstrum = ImageTk.PhotoImage(Image.open("./images/uparrow.png"))
downstrum = ImageTk.PhotoImage(Image.open("./images/downarrow.png"))
select_file_image = ImageTk.PhotoImage(Image.open("./images/select_file.png"))
play_button_image = ImageTk.PhotoImage(Image.open("./images/play-64.png"))
pause_button_image = ImageTk.PhotoImage(Image.open("./images/pause-64.png"))
restart_button_image = ImageTk.PhotoImage(Image.open("./images/rewind-64.png"))
    
downstrum_label1 = Label(image=downstrum,height=100,width=100)
downstrum_label2 = Label(image=downstrum,height=100,width=100)
#downstrum_label1.config(bg="green", fg="green")
    
downstrum_label1.image = downstrum
downstrum_label2.image = downstrum
    
upstrum_label1 = Label(image=upstrum,height=100,width=100)
upstrum_label2 = Label(image=upstrum,height=100,width=100)
    
upstrum_label1.image = upstrum
upstrum_label2.image = upstrum
    
downstrum_label3 = Label(image=downstrum,height=100,width=100)
downstrum_label3.image = downstrum
    
upstrum_label3 = Label(image=upstrum,height=100,width=100)
upstrum_label3.image = upstrum
#######################################################################


############################## FUNCTIONS ########################################

def openFile():
    select_file_button.configure(bg="green")
    play_button.configure(bg=colors["magicMint"])
    stop_button.configure(bg=colors["magicMint"])
    restart_button.configure(bg=colors["magicMint"])
    root.update()
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
    global playFlag
    
    # if(play_button.configure(image=play_button_image)):
    #     playFlag == 1
    
    # if pauseFlag == 1:
    #     play_button.configure(image=play_button_image)
    #     root.update()
        
    #     mixer.music.pause()

    #     if metroOnFlag and metroInit:
    #         metro.pause()

    #     pauseFlag = 0
    #     playFlag = 1
    
#    if playFlag == 1:
    playFlag = 1
    play_button.configure(bg="green")
    stop_button.configure(bg=colors["magicMint"])
    restart_button.configure(bg=colors["magicMint"])
    select_file_button.configure(bg=colors["magicMint"])
    root.update()
    if soundFile:
        songTime = mixer.music.get_pos() // 10
        strums, times = generate_strums()
        if pauseFlag == 1:
            if metroOnFlag and metro != None:
                metro.unpause(metro.calculate_bpm(soundFile), songTime)

            mixer.music.unpause()
        else:
                mixer.music.play()
        root.update()
#        if songTime in strums.keys():
#            if strums[songTime] == "up":
        while playFlag == 1:
            if metroStrumFlag and metroInit:
                metro.strum("down")
            upstrum_label3.config(bg="white",fg="white")
            downstrum_label1.config(bg="green",fg="green")
            time.sleep(0.4)
            root.update()
            if playFlag == 0:
                downstrum_label1.config(bg="white",fg="white")
                root.update()
                break

            if metroStrumFlag and metroInit:
                metro.strum("down")
            downstrum_label1.config(bg="white",fg="white")
            downstrum_label2.config(bg="green",fg="green")
            time.sleep(0.2)
            root.update()
            if playFlag == 0:
                downstrum_label2.config(bg="white",fg="white")
                root.update()
                break
#           else:
            if metroStrumFlag and metroInit:
                metro.strum("up")
            downstrum_label2.config(bg="white",fg="white")
            upstrum_label1.config(bg="green", fg="green")
            time.sleep(0.5)
            root.update()
            if playFlag == 0:
                upstrum_label1.config(bg="white",fg="white")
                root.update()
                break

            if metroStrumFlag and metroInit:
                metro.strum("up")
            upstrum_label1.config(bg="white", fg="white")
            upstrum_label2.config(bg="green",fg="green")
            time.sleep(0.2)
            root.update()
            if playFlag == 0:
                upstrum_label2.config(bg="white",fg="white")
                root.update()
                break

            if metroStrumFlag and metroInit:
                metro.strum("down")
            upstrum_label2.config(bg="white",fg="white")
            downstrum_label3.config(bg="green",fg="green")
            time.sleep(0.2)
            root.update()
            if playFlag == 0:
                downstrum_label3.config(bg="white",fg="white")
                root.update()
                break

            if metroStrumFlag and metroInit:
                metro.strum("up")
            downstrum_label3.config(bg="white",fg="white")
            upstrum_label3.config(bg="green",fg="green")
            time.sleep(0.2)
            root.update()

            if playFlag == 0:
                downstrum_label3.config(bg="white",fg="white")
                root.update()
                break

            if metroOnFlag and metroInit:
                metro.set_bpm(metro.calculate_bpm(soundFile))
                metro.play()
                    

def pause():
    global pauseFlag
    global metroOnFlag
    global playFlag

    mixer.music.pause()

    if metroOnFlag and metroInit:
        metro.pause()
        
    stop_button.configure(bg="green")
    play_button.configure(bg=colors["magicMint"])
    restart_button.configure(bg=colors["magicMint"])
    select_file_button.configure(bg=colors["magicMint"])
    root.update()

    pauseFlag = 1
    playFlag = 0

def restart():
    global pauseFlag
    global metroOnFlag
    global playFlag
    
    restart_button.configure(bg="green")
    stop_button.configure(bg=colors["magicMint"])
    play_button.configure(bg=colors["magicMint"])
    select_file_button.configure(bg=colors["magicMint"])
    root.update()

    if soundFile:
        mixer.music.stop()
        pauseFlag = 0

    if metroOnFlag and metro != None:
        metro.pause()

    playFlag = 0

# def openNotes():
#     generateNotes(soundFile)
#     startfile("notes.txt")


def serial():
    global metroOnFlag
    global metroInit
    port = simpledialog.askstring(title="Select Port",
                                  prompt="Port:")
    metro.set_serial(port)
    metroOnFlag = 0 
    metroInit = 1


def start_metronome():
    global metroOnFlag

    metroOnFlag = 1

    if metro != None:
        metro.set_bpm(metro.calculate_bpm(soundFile))


def pause_metronome():
    global metroOnFlag

    metroOnFlag = 0
    if metro != None:
        metro.pause()

def metronome_strum_en():
    global metroStrumFlag
    metroStrumFlag = 1

def metronome_strum_disen():
    global metroStrumFlag
    metroStrumFlag = 0
        
def display_strum_pattern():
    downstrum_label1.place(x=100,y=450)
    downstrum_label2.place(x=350,y=450)
    upstrum_label1.place(x=600,y=450)
    upstrum_label2.place(x=850,y=450)
    downstrum_label3.place(x=1100,y=450)
    upstrum_label3.place(x=1350,y=450)
    
#def play_strums():
    
    
        
# def display_strums():
#    upstrum = ImageTk.PhotoImage(Image.open("uparrow.png"))
#    downstrum = ImageTk.PhotoImage(Image.open("downarrow.png"))
    
#    downstrum_label1 = Label(image=downstrum,height=100,width=100)
#    downstrum_label2 = Label(image=downstrum,height=100,width=100)
    
#    downstrum_label1.image = downstrum
#    downstrum_label2.image = downstrum
    
#    upstrum_label1 = Label(image=upstrum,height=100,width=100)
#    upstrum_label2 = Label(image=upstrum,height=100,width=100)
    
#    upstrum_label1.image = upstrum
#    upstrum_label2.image = upstrum
    
#    downstrum_label3 = Label(image=downstrum,height=100,width=100)
#    downstrum_label3.image = downstrum
    
#    upstrum_label3 = Label(image=upstrum,height=100,width=100)
#    upstrum_label3.image = upstrum
    
    # infinite loop
#    while True:
#        xaxis = 1550
#        while xaxis > 0:
#            downstrum_label1.place(x=xaxis,y=450)
#            downstrum_label2.place(x=xaxis+250,y=450)
#            upstrum_label1.place(x=xaxis+500,y=450)
#            upstrum_label2.place(x=xaxis+750,y=450)
#            downstrum_label3.place(x=xaxis+1000,y=450)
#            upstrum_label3.place(x=xaxis+1250,y=450)
            
#            root.update()
#            time.sleep(0.00000005)            
#            xaxis-=1        


##################################################################################
##################### ORIGINAL SONG ####################################
button_width_apart = 400

original_song_label = Label(root, text="Original Song", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
original_song_label.place(y=120, x=650)     # x = 90 before

select_file_button = Button(root, text="Select File", font=(
    "Helvetica", 16), relief=GROOVE, command=openFile, bg=colors["magicMint"], image=select_file_image, borderwidth=0)
select_file_button.place(y=200, x=100)

# making a button which trigger the function so sound can be played
play_button = Button(root, text="Play Song", font=(
    "Helvetica", 16), relief=GROOVE, command=play, bg=colors["magicMint"], image=play_button_image, borderwidth=0)
play_button.place(y=200, x=100+button_width_apart)

stop_button = Button(root, text="Pause Song", font=(
    "Helvetica", 16), relief=GROOVE, command=pause, bg=colors["magicMint"], image=pause_button_image, borderwidth=0)
stop_button.place(y=200, x=100+(2*button_width_apart))

restart_button = Button(root, text="Restart Song", font=(
    "Helvetica", 16), relief=GROOVE, command=restart, bg=colors["magicMint"], image=restart_button_image, borderwidth=0)
restart_button.place(y=200, x=100+(3*button_width_apart))

#########################################################################


###################### GENERATING STRUM PATTERNS ########################
strum_pattern_label = Label(root, text="Strum Pattern", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
strum_pattern_label.place(y=300, x=650)

# TO DO: Add functionality on press
generate_patterns_button = Button(root, text="Generate Strum Patterns", font=(
    "Helvetica", 16), relief=GROOVE, command=display_strum_pattern,bg=colors["languidLavender"])
generate_patterns_button.place(y=380, x=100)

#generate_patterns_button = Button(root, text="Generate Notes", font=(
#    "Helvetica", 16), relief=GROOVE, command=openNotes, bg=colors["languidLavender"])
#generate_patterns_button.place(y=380, x=900) #was x=670

# TO DO: Add functionality on press
#start_button = Button(root, text="Start", font=(
#    "Helvetica", 16), relief=GROOVE, command=play_strums, bg=colors["languidLavender"])
#start_button.place(y=380, x=550)

#show_graph_button = Button(root, text="Show Plot", font=(
#    "Helvetica", 16), relief=GROOVE, command=show_graph, bg=colors["languidLavender"])
#show_graph_button.place(y=380, x=1300)

#########################################################################


######################### METRONOME #####################################
buttons_width_apart = 50

metronome_label = Label(root, text="Metronome", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
metronome_label.place(y=600, x=670)

select_serial_port_button = Button(root, text="Select Port", font=(
    "Helvetica", 16), relief=GROOVE, command=serial, bg=colors["mustard"])
select_serial_port_button.place(y=675, x=100)

start_metronome_button = Button(root, text="Metronome Enable", font=(
    "Helvetica", 16), relief=GROOVE, command=start_metronome, bg=colors["mustard"])
start_metronome_button.place(y=675, x=100+button_width_apart)

stop_metronome_button = Button(root, text="Metronome Disable", font=(
    "Helvetica", 16), relief=GROOVE, command=pause_metronome, bg=colors["mustard"])
stop_metronome_button.place(y=675, x=100+2*button_width_apart)

metronome_strum_on_button = Button(root, text="Strums Enable", font=(
    "Helvetica", 16), relief=GROOVE, command=metronome_strum_en, bg=colors["mustard"])
metronome_strum_on_button.place(y=675, x=100+3*button_width_apart)

metronome_strum_off_button = Button(root, text="Strums Disable", font=(
    "Helvetica", 16), relief=GROOVE, command=metronome_strum_disen, bg=colors["mustard"])
metronome_strum_off_button.place(y=750, x=700)
#########################################################################

root.mainloop()
