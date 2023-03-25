# STRUMFINDER

                                Instructions to Navigate the Beta Build
                                
Enter the home directory of the project (where main.py is placed) and run "python main_release_candidate.py".
Use the “Select File” button to select the MIDI file “slow.mid” in the audio-files folder. Click “Play”, then the “Generate Strum Pattern” button to show the strum pattern of the song. If a sliding display of the strums is wanted, select “Sliding Display” instead. If the metronome functionality is wanted, select the “Select Port” button and put in the port the metronome is connected to. The microcontroller should be connected to the piezo as shown in the “Hardware Schematics” document. To enable the metronome click the button that says “Disabled”. The metronome can be used to hear the strum pattern more clearly by clicking the button under mode so that it says “Strums”.



                                                Usability
        Interface
The Original Song section has the Select File, Play, Pause, and Restart Song buttons. The Select File button allows for users to choose a song file with a .mid extension to generate strum patterns for. The Play Song button plays the song and if the metronome is enabled, the metronome will play with it. The Pause Song button pauses the song and the metronome if enabled. The Restart Song button pauses and restarts the song and the metronome if enabled.

The Strum Pattern section has the “Generate Strum Patterns” button. This allows the user to see the strum pattern being used in the song currently. The above image is the Strum Pattern section without anything loaded. Once a song is chosen it can be clicked before it plays to generate the static strum patterns. The “Sliding Display” button is a feature that shows the strums on the screen moving from right to left, as the song is playing. When the “Generate Strum Patterns” button is pressed in the Original Song section, then the “Play” button is pressed, it will generate and display the current strum pattern detected. It only displays six strums at a time then it switches to the next strum pattern once the last strum of the previous one was played in the song. If the metronome strum mode is enabled the metronome will play a down-strum or up-strum noise with the strum. When the “Sliding Display” button is pressed, and then the “Play” button is pressed, the generated strum pattern will be shown moving from right to left, until the strums in the song are over. There is also a triangle marker that is used to signify when to play the current strum.

The Metronome section has the Select Port, Enabled/Disabled, Metronome/Strums buttons. The Select Port button has a dialog box popup that has the user connect to the metronome serially using the port it is connected to. The Enabled/Disabled button enables or disables the metronome. The button toggles between the two. The button under mode is the Metronome/Strums button. If the metronome mode is on then the circuit will just play the circuit like a metronome to the beat of the song. If the strums mode is on then the circuit will play a sound corresponding to an upstrum or downstrum when it happens in the song to make it more noticeable to the user. The above picture shows that the circuit is completely disabled, but it would be in metronome mode if it were enabled.


        Navigation
There is only one screen with buttons that are well defined. The buttons were explained in the above section. All the buttons work as intended - this was done through testing of edge cases to find out if any buttons do not perform as intended when a previous button is pressed. 

        Perception
There is only one screen with buttons that are well defined. Users should easily be able to understand what the buttons do and how to use them. We believe that the UI is easily navigable by users by testing it with friends. In “Generate Strum Patterns” mode, six strums are shown at a time so as to not overwhelm the screen. When a strum is played it has a green box put around it to show the user which strum is currently happening. In “Sliding Display” mode, the strums move from right to left and become highlighted green when they pass the triangle marker, which tells the user that is the current strum.



        Responsiveness

The buttons show when they are clicked so users know that buttons are being responsive. All the buttons are very responsive otherwise. We have worked to make sure that there are no busy waiting loops.
When buttons are pressed in different orders, such as interchanging between stationary strum mode and sliding display mode, we make sure they perform as intended and no overlap occurs.




                                                Build Quality
        Robustness
From our testing, no crashes have happened from edge cases or regular use. Tkinter is a very robust UI since it is simple, and it has not had a problem with unusual input. The metronome is very robust as we saw while testing it. Using a persistent state to connect to it makes sure that there is no unusual value sent to it.

        Consistency
All buttons act predictably. The metronome is very consistent and does not have unusual behavior.  MIDI file input is very consistent as notes are explicitly defined in time and pitch.  Some files have chords described by notes with the same start time, making strum detection difficult.  MIDI files can also define multiple instruments, so currently all of the instruments are combined. 

        Aesthetic Rigor
The aesthetic does not interfere with the functionality of the project. None of the buttons are unresponsive and no buttons or images interfere with the pressing of another button. The circuit is really easy for the user to create and there should be no problem setting it up if they choose to do so.


        Features
        External Interface
The GUI connects to a function that generates the strum pattern. This is the persistent state that connects to the internal systems. The GUI also connects to the metronome class which drives the metronome and sends commands to the microcontroller to tell the metronome what to do. The GUI is able to show the strum patterns well and denotes it in a clear way to the user. It only accepts MIDI files right now to help with the strum detection.

        Persistent State
The user can load a locally stored MIDI file in the GUI.  This will be passed to the internal signal processing systems and the external user interface as playable audio with a metronome and strum patterns.
The metronome class is used to drive the metronome. It sends predefined commands to control the metronome. This class is used by the GUI to interact with the metronome without sending any undefined functions for the microcontroller to do.
The persistent state sends an array of Chord objects which has the type of strum, name of the chord, and the time that it happens. The array is sorted by time so that it can be traversed easily in the GUI to show the strums as the song is playing. The code checks to make sure that the time of the sixth strum is prior to the time happening now, and if it is not it goes to the next strum. This works consistently because the code is fast so it is able to keep track of when each strum happens so that it can show it using the green box. For the sliding display, an algorithm was created so the strums are displayed and moved based on the timing of the song, and when they reach the triangle marker, the outline of the box is turned to green, to indicate it is the current strum.


        Internal Systems
The release candidate automatically detects strums by analyzing MIDI (.mid) files. MIDI files contain explicit definitions of notes that make transcription and strum detection much better than noisy .wav audio files. The midi_strums.py file takes in the filename from the persistent state and returns an array of Chord objects that define a chord’s time within a song, its strum direction, and the name of the chord played. Strums are determined by the order and concurrency of notes and chord names by analyzing the combination and intervals of concurrent notes. Notes are defined by conventional music notation by processing their frequency.  All the instruments contained in the midi file are combined into one with all of their notes as there are often multiple guitars in a file.
The metronome microcontroller code connects serially to the computer. It receives commands from the metronome class. The microcontroller interacts with the piezo to make a metronome and strumming sounds.

