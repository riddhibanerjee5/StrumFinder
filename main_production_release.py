import time
import pygame
from metronome import metronome
from playsound import playsound
from os import startfile
from tkinter import *
import multiprocessing
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image
from pygame import mixer
from midi_strums import generateStrums, getMidiBpm
mixer.init()
pygame.init()

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
metroStrumFlag = 0
playFlag = 0
metroInit = 0
soundFile = None
slidingFlag = 0
displayStrumFlag = 0
generateStrumPressCounter = 0
strum_labels = list()
start_display_strum = list()
screen_width = root.winfo_screenwidth()
strum_pixel_hit = 400
fps = 15
spf = 1 / fps
time_across_screen = 0
start_display_strum = list()
isSlidingDisplayPressed = 0

################################################ Images ##########################################################################
upstrum = ImageTk.PhotoImage(Image.open("./images/uparrow_edit2.jpg"))
downstrum = ImageTk.PhotoImage(Image.open("./images/downarrow_edit2.jpg"))
select_file_image = ImageTk.PhotoImage(Image.open("./images/select_file.png"))
play_button_image = ImageTk.PhotoImage(Image.open("./images/play-green.png").resize((75,75)))
pause_button_image = ImageTk.PhotoImage(Image.open("./images/pause-green.png").resize((75,75)))
restart_button_image = ImageTk.PhotoImage(Image.open("./images/restart_green.png").resize((75,75)))
triangle = ImageTk.PhotoImage(Image.open("./images/triangle.png"))

strumHitTriangle = Label(image=triangle)
strumHitTriangle.image = triangle
strumHitTriangle.config(bg="white")

##################################################################################################################################


################################################# FUNCTIONS ######################################################################

def openFile():
    global strum_labels
    global strums
    global time_across_screen
    global start_display_strum
    global strum_pixel_hit

    select_file_button.configure(bg="green")
    play_button.configure(bg=["white"])
    stop_button.configure(bg=["white"])
    restart_button.configure(bg=colors["white"])
    root.update()
    global soundFile
    global playSound
    soundFile = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("midi files",
                                                      "*.mid*",),("wav files", "*.wav")
                                                      ))
    playSound = mixer.music.load(soundFile)
    
    strums = generateStrums(soundFile, True)

    delay = 2.6
    if len(strum_labels) != 0:
        for strum in strum_labels:
            strum.place(x=6000,y=450)
        root.update()

    start_display_strum.clear()
    strum_labels.clear()

    for i in range(0,len(strums)):
        #print(len(strums[i].notes))
        if(len(strums[i].notes) > 2):
            if(strums[i].strum == False):
                strum_labels.append(Label(image=downstrum,height=99,width=61))
                strum_labels[len(strum_labels)-1].image = downstrum
                strum_labels[len(strum_labels)-1].config(bg="white", fg="white")
                start_display_strum.append(int((strums[i].start - delay) * 1000 // 10))
                #print(strums[ i].start)
                #print(strums[i].start - time_across_screen)
    
            else:
                strum_labels.append(Label(image=upstrum,height=99,width=61))
                strum_labels[len(strum_labels)-1].image = upstrum
                strum_labels[len(strum_labels)-1].config(bg="white", fg="white")
                start_display_strum.append(int((strums[i].start - delay) * 1000 // 10))

    
def play():
    global pauseFlag
    global metroOnFlag
    global playFlag
    global displayStrumFlag
    global slidingFlag
    
    playFlag = 1
    play_button.configure(bg="green")
    stop_button.configure(bg=["white"])
    restart_button.configure(bg=["white"])
    select_file_button.configure(bg=["white"])
    root.update()

    if soundFile:
        songTime = mixer.music.get_pos() // 10
        if pauseFlag == 1:
            if metroOnFlag and metro != None and not metroStrumFlag:
                if (soundFile.find(".wav") != -1):
                    metro.unpause(metro.calculate_bpm(soundFile), songTime)
                else:
                    metro.unpause(getMidiBpm(soundFile), songTime)

            mixer.music.unpause()
        else:
            if metroOnFlag and metro != None and not metroStrumFlag:
                if (soundFile.find(".wav") != -1):
                    metro.set_bpm(metro.calculate_bpm(soundFile))
                else:
                    metro.set_bpm(getMidiBpm(soundFile))
                metro.play()
            mixer.music.play()
        root.update()
        
        print(slidingFlag)
        if displayStrumFlag:
            display_strum_pattern()
        elif slidingFlag:
            display_sliding_strum_pattern()
 

def pause():
    global pauseFlag
    global metroOnFlag
    global playFlag
    global slidingFlag

    mixer.music.pause()

    if metroOnFlag and metroInit:
        metro.pause()
        
    stop_button.configure(bg="green")
    play_button.configure(bg=colors["white"])
    restart_button.configure(bg=colors["white"])
    select_file_button.configure(bg=colors["white"])
    root.update()

    pauseFlag = 1
    playFlag = 0

def restart():
    global pauseFlag
    global metroOnFlag
    global playFlag
    
    restart_button.configure(bg="green")
    stop_button.configure(bg=colors["white"])
    play_button.configure(bg=colors["white"])
    select_file_button.configure(bg=colors["white"])
    root.update()

    for strum in strum_labels:
        strum.place(x=6000,y=450)

    if soundFile:
        mixer.music.stop()
        pauseFlag = 0

    if metroOnFlag and metro != None:
        metro.pause()

    playFlag = 0

def serial():
    global metroOnFlag
    global metroInit
    port = simpledialog.askstring(title="Select Port",
                                  prompt="Port:")
    metro.set_serial(port)
    metroOnFlag = 0 
    metroInit = 1


def metronome_en():
    global metroOnFlag

    if metroOnFlag:
        metroOnFlag = 0
        start_metronome_button.config(text='Disabled')

        if metro != None:
            metro.pause()
    else:
        metroOnFlag = 1
        start_metronome_button.config(text='Enabled')

        if metro != None:
            if (soundFile.find(".wav") != -1):
                metro.set_bpm(metro.calculate_bpm(soundFile))
            else:
                metro.set_bpm(getMidiBpm(soundFile))

    root.update()
    
def metronome_mode_en():
    global metroStrumFlag

    if metroStrumFlag:
        metroStrumFlag = 0
        metronome_mode_button.config(text='Metronome')
    else:
        metroStrumFlag = 1
        metronome_mode_button.config(text='Strums')

    root.update()
        
def display_strum_pattern():
    global soundFile
    global playFlag
    global metroStrumFlag
    global displayStrumFlag
    global slidingFlag
    global generateStrumPressCounter
    global strumHitTriangle
    global strums
    global strum_labels   
    
    displayStrumFlag = 1
    slidingFlag = 0

    #print("displayStrumFlag before: ", displayStrumFlag, " slidingFlag before: ", slidingFlag)
    if(displayStrumFlag == 1 and slidingFlag == 0):
        if soundFile:
            generateStrumPressCounter+=1        # used for tracking play/pause functionality
            strumHitTriangle.place(x=-1500,y=400)
            for j in range(len(strum_labels)):
                strum_labels[j].place(x=1550,y=2000)
                strum_labels[j].config(bg="white",fg="white")
            
            iter = len(strums) // 6
            
            #print("Iter: ", iter)
            last_strum = -1
            music_time = mixer.music.get_pos() // 10

            for i in range(0,iter):
                strum_labels[i*6+0].place(x=100,y=450)
                strum_labels[i*6+1].place(x=350,y=450)
                strum_labels[i*6+2].place(x=600,y=450)
                strum_labels[i*6+3].place(x=850,y=450)
                strum_labels[i*6+4].place(x=1100,y=450)
                strum_labels[i*6+5].place(x=1350,y=450)

               
                root.update()
                    
                #print('playFlag: ', playFlag, ', music time: ', music_time, ', strums[5]: ', strums[i*6+5].start)
                while(playFlag and music_time < (strums[i*6+6].start * 1000 // 10) and displayStrumFlag == 1):
                    music_time = mixer.music.get_pos() // 10

                    for j in range(0, 5):
                        if music_time < (strums[i*6+j+1].start * 1000 // 10) and music_time >= (strums[i*6+j].start * 1000 // 10):
                            if j == 0:
                                strum_labels[i*6+5].config(bg="white",fg="white")
                                strum_labels[i*6+0].config(bg="green",fg="green")

                                if metroOnFlag and metroStrumFlag:
                                    if last_strum != 0:
                                        if strums[i*6].strum:
                                            metro.strum('up')
                                        else:
                                            metro.strum('down')
                                    
                                    last_strum = 0

                            elif j == 1:
                                strum_labels[i*6+0].config(bg="white",fg="white")
                                strum_labels[i*6+1].config(bg="green",fg="green")

                                if metroStrumFlag and metroOnFlag:
                                    if last_strum != 1:
                                        if strums[i*6+1].strum:
                                            metro.strum('up')
                                        else:
                                            metro.strum('down')
                                    
                                    last_strum = 1

                            elif j == 2:
                                strum_labels[i*6+1].config(bg="white",fg="white")
                                strum_labels[i*6+2].config(bg="green",fg="green")

                                if metroStrumFlag and metroOnFlag:
                                    if last_strum != 2:
                                        if strums[i*6+2].strum:
                                            metro.strum('up')
                                        else:
                                            metro.strum('down')
                                    
                                    last_strum = 2

                            elif j == 3:
                                strum_labels[i*6+2].config(bg="white",fg="white")
                                strum_labels[i*6+3].config(bg="green",fg="green")

                                if metroStrumFlag and metroOnFlag:
                                    if last_strum != 3:
                                        if strums[i*6+3].strum:
                                            metro.strum('up')
                                        else:
                                            metro.strum('down')
                                    
                                    last_strum = 3

                            elif j == 4:
                                strum_labels[i*6+3].config(bg="white",fg="white")
                                strum_labels[i*6+4].config(bg="green",fg="green")

                                if metroStrumFlag and metroOnFlag:
                                    if last_strum != 4:
                                        if strums[i*6+4].strum:
                                            metro.strum('up')
                                        else:
                                            metro.strum('down')
                                    
                                    last_strum = 4

                            elif j == 5:
                                strum_labels[i*6+4].config(bg="white",fg="white")
                                strum_labels[i*6+5].config(bg="green",fg="green")

                                if metroStrumFlag and metroOnFlag:
                                    if last_strum != 5:
                                        if strums[i*6+5].strum:
                                            metro.strum('up')
                                        else:
                                            metro.strum('down')
                                    
                                    last_strum = 5

                    if music_time < (strums[i*6+6].start * 1000 // 10) and music_time >= (strums[i*6+5].start * 1000 // 10):
                        strum_labels[i*6+4].config(bg="white",fg="white")
                        strum_labels[i*6+5].config(bg="green",fg="green")

                        if metroStrumFlag and metroOnFlag:
                            if last_strum != 5:
                                if strums[i*6+5].strum:
                                    metro.strum('up')
                                else:
                                    metro.strum('down')
                            
                            last_strum = 5

                    root.update()

                if playFlag == False:
                    break
                if displayStrumFlag == False:
                    break
                    
            root.update()
        
def display_sliding_strum_pattern():
    global slidingFlag
    global displayStrumFlag
    global root
    global isSlidingDisplayPressed
    global strums
    global strum_labels
    global strumHitTriangle
    global time_across_screen
    
    isSlidingDisplayPressed+=1
    slidingFlag = 1
    displayStrumFlag = 0

    clock = pygame.time.Clock()
    
    if soundFile:
        strumHitTriangle.place(x=410,y=375)

        #print("Counter: ", isSlidingDisplayPressed)
        if(isSlidingDisplayPressed > 1):
            for j in range(len(strum_labels)):
                strum_labels[j].place(x=1550,y=2000)
                strum_labels[j].config(bg="white",fg="white")
                
        root.update()
        #print(int(spf*1000))
        while mixer.music.get_pos() != -1 and mixer.music.get_pos() < strums[len(strums)-1].start * 1000 + 1 and slidingFlag == 1:
            sliding_animation()
            clock.tick(60)
            #print(clock.get_fps())
        
        

def sliding_animation():
    global strum_labels
    global start_display_strum
    global slidingFlag 
    global displayStrumFlag
    global strum_pixel_hit
    global strums
    global metroOnFlag
    global metroStrumFlag

    window_width = root.winfo_screenwidth()
    music_time = mixer.music.get_pos() // 10
    for i in range(len(start_display_strum)):
        if music_time >= start_display_strum[i] and music_time - start_display_strum[i] < 460:
            #print("music time: ", music_time, ", strums time: ", start_display_strum[i], ", pixel: ", (window_width - ((music_time - start_display_strum[i]) * 5), ", window: ", window_width))
            x_pixel = int(window_width - ((music_time - start_display_strum[i]) * 4))

            strum_labels[i].place(x=x_pixel,y=450)
            if x_pixel <= strum_pixel_hit:
                strum_labels[i].config(bg="green",fg="green")

            if x_pixel - strum_pixel_hit < 5 and x_pixel - strum_pixel_hit > -5:
                if metroStrumFlag and metroOnFlag:
                    if strums[i].strum:
                        metro.strum('up')
                    else:
                        metro.strum('down')

    root.update()

#################################################################################################################################


################################################ ORIGINAL SONG ##################################################################
button_width_apart = 400

original_song_label = Label(root, text="Original Song", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
original_song_label.place(y=120, x=650)     # x = 90 before

select_file_button = Button(root, text="Select File", font=(
    "Helvetica", 16), relief=GROOVE, command=openFile, bg=colors["magicMint"], image=select_file_image, borderwidth=0)
select_file_button.place(y=200, x=100)

# making a button which trigger the function so sound can be played
play_button = Button(root, text="Play Song", font=(
    "Helvetica", 16), relief=GROOVE, command=play, bg=colors["white"], image=play_button_image, borderwidth=0)
play_button.place(y=200, x=100+button_width_apart)

stop_button = Button(root, text="Pause Song", font=(
    "Helvetica", 16), relief=GROOVE, command=pause, bg=colors["white"], image=pause_button_image, borderwidth=0)
stop_button.place(y=200, x=100+(2*button_width_apart))

restart_button = Button(root, text="Restart Song", font=(
    "Helvetica", 16), relief=GROOVE, command=restart, bg=colors["white"], image=restart_button_image, borderwidth=0)
restart_button.place(y=200, x=100+(3*button_width_apart))

################################################################################################################################


############################################## GENERATING STRUM PATTERNS #######################################################
strum_pattern_label = Label(root, text="Strum Pattern", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
strum_pattern_label.place(y=300, x=650)

generate_patterns_button = Button(root, text="Generate Strum Patterns", font=(
    "Helvetica", 16), relief=GROOVE, command=display_strum_pattern,bg=colors["languidLavender"])
generate_patterns_button.place(y=380, x=100)

sliding_display_button = Button(root, text="Sliding Display", font=(
    "Helvetica", 16), relief=GROOVE, command=display_sliding_strum_pattern,bg=colors["languidLavender"])
sliding_display_button.place(y=380, x=685)

#################################################################################################################################


############################################## METRONOME ########################################################################

metronome_label = Label(root, text="Metronome", font=(
    "Helvetica", 25, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
metronome_label.place(y=600, x=670)

select_serial_port_button = Button(root, text="Select Port", font=(
    "Helvetica", 16), relief=GROOVE, command=serial, bg=colors["mustard"])
select_serial_port_button.place(y=675, x=100)

start_metronome_button = Button(root, text="Disabled", font=(
    "Helvetica", 16), relief=GROOVE, command=metronome_en, bg=colors["mustard"])
start_metronome_button.place(y=675, x=715)

metronome_mode_label = Label(root, text="Mode", font=(
    "Helvetica", 16, "bold"), bg=colors["white"], fg=colors["orangeSoda"])
metronome_mode_label.place(y=630, x=1225)

metronome_mode_button = Button(root, text="Metronome", font=(
    "Helvetica", 16), relief=GROOVE, command=metronome_mode_en, bg=colors["mustard"])
metronome_mode_button.place(y=675, x=1200)

#################################################################################################################################

root.mainloop()
