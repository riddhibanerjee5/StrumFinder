import time
from metronome import metronome
from playsound import playsound
from os import startfile
from tkinter import *
import multiprocessing
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image
from pygame import mixer
from midi_strums import generateStrums, getMidiBpm
#from stft_chirp import show_graph
#from stft import generateNotes
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
soundFile = None

################################################ Images ##########################################################################
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
play_button_image = ImageTk.PhotoImage(Image.open("./images/play-green.png").resize((75,75)))
pause_button_image = ImageTk.PhotoImage(Image.open("./images/pause-green.png").resize((75,75)))
restart_button_image = ImageTk.PhotoImage(Image.open("./images/restart_green.png").resize((75,75)))


    
# At most, can have six of the same strums on the screen at a time
downstrum_label1 = Label(image=downstrum,height=100,width=100)
downstrum_label2 = Label(image=downstrum,height=100,width=100)
downstrum_label3 = Label(image=downstrum,height=100,width=100)
downstrum_label4 = Label(image=downstrum,height=100,width=100)
downstrum_label5 = Label(image=downstrum,height=100,width=100)
downstrum_label6 = Label(image=downstrum,height=100,width=100)
    
downstrum_label1.image = downstrum
downstrum_label2.image = downstrum
downstrum_label3.image = downstrum
downstrum_label4.image = downstrum
downstrum_label5.image = downstrum
downstrum_label6.image = downstrum
    
upstrum_label1 = Label(image=upstrum,height=100,width=100)
upstrum_label2 = Label(image=upstrum,height=100,width=100)
upstrum_label3 = Label(image=upstrum,height=100,width=100)
upstrum_label4 = Label(image=upstrum,height=100,width=100)
upstrum_label5 = Label(image=upstrum,height=100,width=100)
upstrum_label6 = Label(image=upstrum,height=100,width=100)
    
upstrum_label1.image = upstrum
upstrum_label2.image = upstrum
upstrum_label3.image = upstrum
upstrum_label4.image = upstrum
upstrum_label5.image = upstrum
upstrum_label6.image = upstrum
    
##################################################################################################################################

################################################# TEST VARIABLES #################################################################

strum1 = [8,8,12,5,20,20] # down, down, up, down, up, up
strum2 = [2,2,2,2,2,11]   # down, down, down, down, down, up
strum3 = [15,15,15,1,1,1] # up, up, up, down, down, down

##################################################################################################################################


################################################# FUNCTIONS ######################################################################

def openFile():
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


def play():
    global pauseFlag
    global metroOnFlag
    global playFlag
    
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
#        if songTime in strums.keys():
#            if strums[songTime] == "up":
        #while playFlag == 1:
        #    if metroStrumFlag and metroInit:
        #        metro.strum("down")
        #    upstrum_label3.config(bg="white",fg="white")
        #    downstrum_label1.config(bg="green",fg="green")
        #    time.sleep(0.4)
        #    root.update()
        #    if playFlag == 0:
        #        downstrum_label1.config(bg="white",fg="white")
        #        root.update()
        #        break
#
        #    if metroStrumFlag and metroInit:
        #        metro.strum("down")
        #    downstrum_label1.config(bg="white",fg="white")
        #    downstrum_label2.config(bg="green",fg="green")
        #    time.sleep(0.2)
        #    root.update()
        #    if playFlag == 0:
        #        downstrum_label2.config(bg="white",fg="white")
        #        root.update()
        #        break
#       #    else:
        #    if metroStrumFlag and metroInit:
        #        metro.strum("up")
        #    downstrum_label2.config(bg="white",fg="white")
        #    upstrum_label1.config(bg="green", fg="green")
        #    time.sleep(0.5)
        #    root.update()
        #    if playFlag == 0:
        #        upstrum_label1.config(bg="white",fg="white")
        #        root.update()
        #        break
#
        #    if metroStrumFlag and metroInit:
        #        metro.strum("up")
        #    upstrum_label1.config(bg="white", fg="white")
        #    upstrum_label2.config(bg="green",fg="green")
        #    time.sleep(0.2)
        #    root.update()
        #    if playFlag == 0:
        #        upstrum_label2.config(bg="white",fg="white")
        #        root.update()
        #        break
#
        #    if metroStrumFlag and metroInit:
        #        metro.strum("down")
        #    upstrum_label2.config(bg="white",fg="white")
        #    downstrum_label3.config(bg="green",fg="green")
        #    time.sleep(0.2)
        #    root.update()
        #    if playFlag == 0:
        #        downstrum_label3.config(bg="white",fg="white")
        #        root.update()
        #        break
#
        #    if metroStrumFlag and metroInit:
        #        metro.strum("up")
        #    downstrum_label3.config(bg="white",fg="white")
        #    upstrum_label3.config(bg="green",fg="green")
        #    time.sleep(0.2)
        #    root.update()
#
        #    if playFlag == 0:
        #        downstrum_label3.config(bg="white",fg="white")
        #        root.update()
        #        break
#
        #    if metroOnFlag and metroInit:
        #        metro.set_bpm(metro.calculate_bpm(soundFile))
        #        metro.play()
                    

def pause():
    global pauseFlag
    global metroOnFlag
    global playFlag

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
    
    #print("Hi")
    #print(soundFile)
    #print(metroStrumFlag)
    if soundFile:
        strums = generateStrums(soundFile)
        
        iter = len(strums) // 6
        
        #print("Iter: ", iter)
        last_strum = -1
        music_time = mixer.music.get_pos() // 10
        for i in range(0,iter):
            #print('i: ', i)
            #print('strums[', i*6 + 0, ']: ', strums[i*6 + 0].strum, ', time: ', strums[i + 0].start)
            #print('strums[', i*6 + 1, ']: ', strums[i*6 + 1].strum, ', time: ', strums[i + 1].start)
            #print('strums[', i*6 + 2, ']: ', strums[i*6 + 2].strum, ', time: ', strums[i + 2].start)
            #print('strums[', i*6 + 3, ']: ', strums[i*6 + 3].strum, ', time: ', strums[i + 3].start)
            #print('strums[', i*6 + 4, ']: ', strums[i*6 + 4].strum, ', time: ', strums[i + 4].start)
            #print('strums[', i*6 + 5, ']: ', strums[i*6 + 5].strum, ', time: ', strums[i + 5].start)

            if(strums[i*6].strum == False):
                #print('down')
                downstrum_label1.place(x=100,y=450)
                upstrum_label1.place(x=6000,y=450)
                #root.update()
            else:
                #print('up')
                upstrum_label1.place(x=100,y=450)
                downstrum_label1.place(x=6000,y=450)
                #root.update()
            
            if(strums[i*6+1].strum):
                #print('up')
                upstrum_label2.place(x=350,y=450)
                downstrum_label2.place(x=6500,y=450)
                #root.update()
            else:
                #print('down')
                downstrum_label2.place(x=350,y=450)
                upstrum_label2.place(x=6500,y=450)
                #root.update()
            
                
            if(strums[i*6+2].strum == False):
                #print('down')
                downstrum_label3.place(x=600,y=450)
                upstrum_label3.place(x=6000,y=450)
                #root.update()
            else:
                #print('up')
                upstrum_label3.place(x=600,y=450)
                downstrum_label3.place(x=6000,y=450)
                #root.update()
                
            if(strums[i*6+3].strum == False):
                #print('down')
                downstrum_label4.place(x=850,y=450)
                upstrum_label4.place(x=8500,y=450)
                #root.update()
            else:
                #print('up')
                upstrum_label4.place(x=850,y=450)
                downstrum_label4.place(x=8500,y=450)
                #root.update()
                
            if(strums[i*6+4].strum == False):
                #print('down')
                downstrum_label5.place(x=1100,y=450)
                upstrum_label5.place(x=11000,y=450)
                #root.update()
            else:
                #print('up')
                upstrum_label5.place(x=1100,y=450)
                downstrum_label5.place(x=11000,y=450)
                #root.update()
                
            if(strums[i*6+5].strum == False):
                #print('down')
                downstrum_label6.place(x=1350,y=450)
                upstrum_label6.place(x=13500,y=450)
                #root.update()
            else:
                #print('up')
                upstrum_label6.place(x=1350,y=450)
                downstrum_label6.place(x=13500,y=450)
                #root.update()
                
            root.update()
                
            #print('playFlag: ', playFlag, ', music time: ', music_time, ', strums[5]: ', strums[i*6+5].start)
            while(playFlag and music_time <= strums[i*6+5].start):
                music_time = mixer.music.get_pos() // 10

                for j in range(0, 5):
                    if music_time < strums[i*6+j+1].start and music_time >= strums[i*6+j].start:
                        #print(j)
                        if j == 0:
                            downstrum_label6.config(bg="white",fg="white")
                            upstrum_label6.config(bg="white",fg="white")

                            downstrum_label1.config(bg="green",fg="green")
                            upstrum_label1.config(bg="green",fg="green")

                            if metroOnFlag and metroStrumFlag:
                                if last_strum != 0:
                                    if strums[i*6].strum:
                                        metro.strum('up')
                                    else:
                                        metro.strum('down')
                                
                                last_strum = 0

                        elif j == 1:
                            downstrum_label1.config(bg="white",fg="white")
                            upstrum_label1.config(bg="white",fg="white")

                            downstrum_label2.config(bg="green",fg="green")
                            upstrum_label2.config(bg="green",fg="green")

                            if metroStrumFlag and metroOnFlag:
                                if last_strum != 1:
                                    if strums[i*6+1].strum:
                                        metro.strum('up')
                                    else:
                                        metro.strum('down')
                                
                                last_strum = 1

                        elif j == 2:
                            downstrum_label2.config(bg="white",fg="white")
                            upstrum_label2.config(bg="white",fg="white")

                            downstrum_label3.config(bg="green",fg="green")
                            upstrum_label3.config(bg="green",fg="green")

                            if metroStrumFlag and metroOnFlag:
                                if last_strum != 2:
                                    if strums[i*6+2].strum:
                                        metro.strum('up')
                                    else:
                                        metro.strum('down')
                                
                                last_strum = 2

                        elif j == 3:
                            downstrum_label3.config(bg="white",fg="white")
                            upstrum_label3.config(bg="white",fg="white")

                            downstrum_label4.config(bg="green",fg="green")
                            upstrum_label4.config(bg="green",fg="green")

                            if metroStrumFlag and metroOnFlag:
                                if last_strum != 3:
                                    if strums[i*6+3].strum:
                                        metro.strum('up')
                                    else:
                                        metro.strum('down')
                                
                                last_strum = 3

                        elif j == 4:
                            downstrum_label4.config(bg="white",fg="white")
                            upstrum_label4.config(bg="white",fg="white")

                            downstrum_label5.config(bg="green",fg="green")
                            upstrum_label5.config(bg="green",fg="green")

                            if metroStrumFlag and metroOnFlag:
                                if last_strum != 4:
                                    if strums[i*6+4].strum:
                                        metro.strum('up')
                                    else:
                                        metro.strum('down')
                                
                                last_strum = 4

                        elif j == 5:
                            downstrum_label5.config(bg="white",fg="white")
                            upstrum_label5.config(bg="white",fg="white")

                            downstrum_label6.config(bg="green",fg="green")
                            upstrum_label6.config(bg="green",fg="green")

                            if metroStrumFlag and metroOnFlag:
                                if last_strum != 5:
                                    if strums[i*6+5].strum:
                                        metro.strum('up')
                                    else:
                                        metro.strum('down')
                                
                                last_strum = 5

                if music_time < strums[i*6+6].start and music_time >= strums[i*6+5].start:
                    downstrum_label5.config(bg="white",fg="white")
                    upstrum_label5.config(bg="white",fg="white")

                    downstrum_label6.config(bg="green",fg="green")
                    upstrum_label6.config(bg="green",fg="green")

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
                
        root.update()
        
    
            
    # downstrum_label1.place(x=100,y=450)
    # downstrum_label2.place(x=350,y=450)
    # upstrum_label1.place(x=600,y=450)
    # upstrum_label2.place(x=850,y=450)
    # downstrum_label3.place(x=1100,y=450)
    # upstrum_label3.place(x=1350,y=450)
    
def play_strums():
    test = 1
    
        
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
