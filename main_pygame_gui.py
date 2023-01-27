from metronome import metronome
from playsound import playsound
from os import startfile
from tkinter import *
import multiprocessing
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image
from stft_chirp import show_graph
from stft import generateNotes
from strum import generate_strums
import pygame, sys

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()

# variables
width =  1600   # width of grid
height = 800    # height of grid
title_font = pygame.font.Font('OVERLOAD.ttf', 64)
font = pygame.font.SysFont('microsoftsansserif', 26, False, False)
subtitle_font = pygame.font.Font('OVERLOAD.ttf', 42)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
metro = metronome()
metro_loaded_flag = False   # if the metronome is connected
strum_showing_flag = False  # if the strum pattern should show
music_playing_flag = False  # if the music is playing
metronome_strum_flag = False    # if the metronome should be used to hear strums
metronome_en = False            # if the metronome is on
bpm = 0
last_strum = False      # keeps track of the last strum to show
already_played = False  # makes sure the metronome only sounds once during strumming
play = False            # if the music will be played 
soundFile = None        # the sound file name
pauseFlag = 0           # if the music is paused

# tkinter for setting up port and getting file name
root = Tk()
root.withdraw()

# more reusable variables
colors = {"background_color" : (0x2d, 0x2d, 0x2b), "font_color" : (0xbb, 0xbf, 0xd5), "white" : (255, 255, 255),
        "title_font_color" : (0xe0, 0x5c, 0xeb)}

img = {"play" : pygame.image.load("images/play-64.png").convert_alpha(), "pause" : pygame.image.load("images/pause-64.png").convert_alpha(),
        "restart" : pygame.image.load("images/rewind-64.png").convert_alpha(), "arrow" : pygame.image.load("images/arrow-141-64.png").convert_alpha()}

buttons = {"sel_file" : pygame.Rect(100, height // 8, 200, 50), "play/pause" : img["play"].get_rect(center = (width // 2, height // 4 + 20)),
            "restart" : img["restart"].get_rect(center = (width // 2 - 200, height // 4 + 20)), "sel_port" : pygame.Rect(1300, height // 8, 200, 50),
            "play_pattern" : img["play"].get_rect(center = (500,500)), "metro" : pygame.Rect(400, height // 8 * 7, 200, 45),
            "metro_mode" : pygame.Rect(700, height // 8 * 7, 200, 50)}


def draw_screen(play):
    screen.fill(colors["background_color"])
    strum_pattern_area = pygame.draw.rect(screen, colors["title_font_color"], (0, 400, 1600, 800))
    metronome_area = pygame.draw.rect(screen, colors["background_color"], (0, 600, 1600, 800))

    # title 
    title = title_font.render('STRUMFINDER', True, colors["title_font_color"])
    title_rect = title.get_rect()
    title_rect.center = (width // 2, height // 8)
    screen.blit(title, title_rect)

    # select file button
    sel_file_button = pygame.draw.rect(screen, colors["title_font_color"], (100, height // 8, 200, 45), border_radius=5)
    sel_file = font.render('Select File', True, colors["white"], colors["title_font_color"])
    sel_file_rect = sel_file.get_rect()
    sel_file_rect.topleft = (140, height // 8 + 8)
    screen.blit(sel_file, sel_file_rect)

    # select port button
    sel_port_button = pygame.draw.rect(screen, colors["title_font_color"], (1300, height // 8, 200, 45), border_radius=5)
    sel_port = font.render('Select Port', True, colors["white"], colors["title_font_color"])
    sel_port_rect = sel_file.get_rect()
    sel_port_rect.topleft = (1340, height // 8 + 8)
    screen.blit(sel_port, sel_port_rect)

    # metronome area
    metro_title = subtitle_font.render("Metronome", True, colors["white"], colors["background_color"])
    metro_title_rect = metro_title.get_rect()
    metro_title_rect.topleft = (105, height // 8 * 7)
    screen.blit(metro_title, metro_title_rect)

    metro_en_str = "Off"
    if metronome_en:
        metro_en_str = "On"
    metro_en_button = pygame.draw.rect(screen, colors["title_font_color"], (400, height // 8 * 7, 200, 45), border_radius=5)   
    metro_en = font.render(metro_en_str, True, colors["white"], colors["title_font_color"])
    metro_en_rect = metro_title.get_rect()
    metro_en_rect.topleft = (480, height // 8 * 7 + 8)
    screen.blit(metro_en, metro_en_rect)

    metro_mode_title = font.render("Mode", True, colors["white"], colors["background_color"])
    metro_mode_title_rect = metro_mode_title.get_rect()
    metro_mode_title_rect.topleft = (770, height // 8 * 7 - 50)
    screen.blit(metro_mode_title, metro_mode_title_rect)

    metro_mode_button = pygame.draw.rect(screen, colors["title_font_color"], (700, height // 8 * 7, 200, 50), border_radius=5)
    metro_button_str = "Normal"
    if metronome_strum_flag:
        metro_button_str = "Strumming"
    metro_mode = font.render(metro_button_str, True, colors["white"], colors["title_font_color"])
    metro_mode_rect = metro_mode.get_rect()
    metro_mode_rect.topleft = (760, height // 8 * 7 + 8)
    screen.blit(metro_mode, metro_mode_rect)

    # strum pattern area
    strum_title = subtitle_font.render("Strum Pattern", True, colors["white"], colors["title_font_color"])
    strum_title_rect = strum_title.get_rect()
    strum_title_rect.topleft = (100, 475)
    screen.blit(strum_title, strum_title_rect)


    if soundFile and play == True:
        screen.blit(img["pause"], buttons["play/pause"])
    else:
        screen.blit(img["play"], buttons["play/pause"])

    screen.blit(img["restart"], buttons["restart"])

    if strum_showing_flag:
        screen.blit(img["pause"], buttons["play_pattern"])
    else:
        screen.blit(img["play"], buttons["play_pattern"])

    
    

    

while True:
    # draw buttons and screen
    draw_screen(play)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if buttons["sel_file"].collidepoint(pos[0], pos[1]):
                
                soundFile = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("wav files",
                                                      "*.wav*"),
                                                      ))
                playSound = pygame.mixer.music.load(soundFile)
                bpm = metro.calculate_bpm(soundFile)

            elif buttons["play/pause"].collidepoint(pos[0], pos[1]):
                if soundFile:
                    play = not play

                    if play and not pauseFlag:
                        pygame.mixer.music.play()
                        pauseFlag = 0
                        music_playing_flag = True
                    elif play and pauseFlag:
                        pygame.mixer.music.unpause()
                        pauseFlag = 0
                        music_playing_flag = True
                    elif not play:
                        pygame.mixer.music.pause()
                        pauseFlag = 1
                        music_playing_flag = False

            elif buttons["restart"].collidepoint(pos[0], pos[1]):
                pauseFlag = 0
                pygame.mixer.music.stop()
                music_playing_flag = False

            elif buttons["sel_port"].collidepoint(pos[0], pos[1]):
                port = simpledialog.askstring(title="Select Port",
                                prompt="Port:")
                metro.set_serial(port)
                metro_loaded_flag = True

            elif buttons["play_pattern"].collidepoint(pos[0], pos[1]):
                strum_showing_flag = not strum_showing_flag
                if soundFile:
                    notes = generateNotes(soundFile)
                    strums, times = generate_strums()

                    

            elif buttons["metro"].collidepoint(pos[0], pos[1]):
                if metro_loaded_flag:
                    metronome_en = not metronome_en

            elif buttons["metro_mode"].collidepoint(pos[0], pos[1]):
                if metro_loaded_flag:
                    metronome_strum_flag = not metronome_strum_flag
            


    if metronome_en and soundFile and not metronome_strum_flag and metro_loaded_flag:
        metro.set_bpm(metro.calculate_bpm(soundFile))
        metro.play()
    elif not metronome_en and metro_loaded_flag:
        metro.pause()
    
    # False = up, True = down
    if music_playing_flag and strum_showing_flag: 
        music_time = pygame.mixer.music.get_pos() // 10
        #print(music_time)

        if music_time in strums.keys():
            if strums[music_time] == "up":
                last_strum = False

                if metronome_strum_flag and metro_loaded_flag and not already_played:
                    metro.strum("up")
                    already_played = True
            else:
                last_strum = True

                if metronome_strum_flag and metro_loaded_flag and not already_played:
                    metro.strum("down")
                    already_played = True
        else:
            already_played = False

            
        arrow_img = img["arrow"].copy()
        if last_strum:
            arrow_img = pygame.transform.flip(arrow_img, False, True)
        rect = arrow_img.get_rect(center = (600,500))

        screen.blit(arrow_img, rect)


            
    pygame.display.update()



pygame.quit()
