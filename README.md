# STRUMFINDER

                                Instructions to Navigate the Beta Build
                                
Enter the home directory of the project (where main.py is placed) and run "python main.py".
Use the Select File button to select the midi file “faster_strums.mid” in the audio-files folder. Click Play, then the Generate Strum Pattern button to show the strum pattern of the song. If the metronome functionality is wanted, select the Select Port button and put in the port the metronome is connected to. The microcontroller should be connected to the piezo as shown in the “Hardware Schematics” document. To enable the metronome click the button that says “Disabled”. The metronome can be used to hear the strum pattern more clearly by clicking the button under mode so that it says “Strums”.


                                                Usability
        Interface
The Original Song section has the Select File, Play, Pause, and Restart Song buttons. The Select File button allows for users to choose a song file with a .mid extension to generate strum patterns for. The Play Song button plays the song and if the metronome is enabled, the metronome will play with it. The Pause Song button pauses the song and the metronome if enabled. The Restart Song button pauses and restarts the song and the metronome if enabled.

The Strum Pattern section has the Generate Strum Patterns button. This allows the user to see the strum pattern being used in the song currently. The above image is the Strum Pattern section without anything loaded. Once a song is chosen it can be clicked before it plays to generate the strum patterns. When the Play Song button is pressed in the Original Song section, then the Generate Strum Patterns button is pressed, it will generate and display the current strum pattern detected. It only displays six strums at a time then it switches to the next strum pattern once the last strum of the previous one was played in the song. If the metronome strum mode is enabled the metronome will play a down-strum or up-strum noise with the strum.

The Metronome section has the Select Port, Enabled/Disabled, Metronome/Strums buttons. The Select Port button has a dialog box popup that has the user connect to the metronome serially using the port it is connected to. The Enabled/Disabled button enables or disables the metronome. The button toggles between the two. The button under mode is the Metronome/Strums button. If the metronome mode is on then the circuit will just play the circuit like a metronome to the beat of the song. If the strums mode is on then the circuit will play a sound corresponding to an upstrum or downstrum when it happens in the song to make it more noticeable to the user. The above picture shows that the circuit is completely disabled, but it would be in metronome mode if it were enabled.


        Navigation
There is only one screen with buttons that are well defined. The buttons were explained in the above section. 
There is a known bug that the generate strums button HAS to be pressed after the play button to work properly. If it is pressed beforehand it won’t show the next strum pattern and it will only show the first one. This bug is a result of not wanting to implement a busy waiting loop to keep checking for if the music is playing. Our idea of how to fix it is to implement a polling method on a flag for if music is being played at the current moment.

        Perception
There is only one screen with buttons that are well defined. Users should easily be able to understand what the buttons do and how to use them. We believe that the UI is easily navigable by users by testing it with friends. The metronome section can be a little confusing, so we plan on implementing a help screen in the future or a simple drop down menu. Six strums are shown at a time as to not overwhelm the screen. When a strum is played it has a green box put around it to show the user which strum is currently happening.


        Responsiveness

The buttons show when they are clicked so users know that buttons are being responsive. All the buttons are very responsive otherwise.
There can be a little delay in playing the midi file. At the moment, we are not sure why this happens and could just be due to pygame being slow for audio. It is not too noticeable and does not take away from the overall experience. We have worked to make sure that there is no busy waiting loops. 



                                                Build Quality
        Robustness
From our testing, no crashes have happened from edge cases or regular use. Tkinter is a very robust UI since it is simple, and it has not had a problem with unusual input. The metronome is very robust as we saw while testing it. Using a persistent state to connect to it makes sure that there is no unusual value sent to it.

Midi file input is very consistent as notes are explicitly defined in time and pitch.  Some files have chords described by notes with the same start time, making strum detection difficult.  Midi files can also define multiple instruments, so logic that selects only the guitar needs to be completed.  Detecting multiple strums and chords within the context of a song has proven to be a difficult signal processing problem and currently the outputs are inconsistent.  When using an audio file of a single strum and only trying to detect a single strum, the output is consistent.  Automatic transcription is also inconsistent due to noise in the guitar signal.

        Consistency
All buttons act predictably. The only time the UI acts unpredictably is during the bug which is described in the Navigation section. The metronome is very consistent and does not have unusual behavior.

        Aesthetic Rigor
The aesthetic does not interfere with the functionality of the project. None of the buttons are unresponsive and no buttons or images interfere with the pressing of another button. The circuit is really easy for the user to create and there should be no problem setting it up if they choose to do so.


        Features
        External Interface
The GUI connects to a function that generates the strum pattern. This is the persistent state that connects to the internal systems. The GUI also connects to the metronome class which drives the metronome and sends commands to the microcontroller to tell the metronome what to do. The GUI is able to show the strum patterns well and denotes it in a clear way to the user. It only accepts MIDI files right now to help with the strum detection.

        Persistent State
The user can load a locally stored MIDI file in the GUI.  This will be passed to the internal signal processing systems and the external user interface as playable audio with a metronome and strum patterns.
The metronome class is used to drive the metronome. It sends predefined commands to control the metronome. This class is used by the GUI to interact with the metronome without sending any undefined functions for the microcontroller to do.
The persistent state sends an array of Chord objects which has the type of strum and the time that it happens. The array is sorted by time so that it can be traversed easily in the GUI to show the strums as the song is playing. The code checks to make sure that the time of the sixth strum is prior to the time happening now, and if it is not it goes to the next strum. This works consistently because the code is fast so it is able to keep track of when each strum happens so that it can show it using the green box.

        Internal Systems
The automatic detection of strum direction using the slope of the time-frequency plane and the automatic transcription of notes using the fundamental frequency method have proven to be difficult problems to solve, largely due to the excess of noise in guitar signals and the resulting challenge of determining note onset.  To move the project forward we have changed the input type from .wav to .mid.  MIDI files contain explicit definitions of notes that make transcription and strum detection much easier and more consistent.  The midi_strums.py file takes in the filename from the persistent state and returns an array of Chord objects that define a chord’s time within a song and its strum direction.  Logic to define the type of chord for a proper transcription will be implemented.  We will flush out our .mid implementation while continuing to look at the possibilities with .wav files.

The metronome microcontroller code connects serially to the computer. It receives commands from the metronome class. The microcontroller interacts with the piezo to make a metronome and strumming sounds.
