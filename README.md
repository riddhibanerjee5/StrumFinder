# STRUMFINDER

        Instructions to Navigate the Alpha Build
Use the Select File button to select the wav file “You and I - Ingrid Michaelson.wav” in the wav-files folder. Click the Generate Strum Pattern button to show the strum pattern of the song. If the metronome functionality is wanted, select the Select Port button and put in the port the metronome is connected to. The microcontroller should be connected to the piezo as shown in the “Hardware Schematics” document. To enable the metronome click the Enable Metronome button. Click the Play Song button to play the song and see how the strum pattern is played within the song. The metronome can be used to hear the strum pattern more clearly by clicking Disable Metronome then Strums Enable button. 


        Usability
        Interface
The Original Song section has the Select File, Play Song, Pause Song, and Restart Song buttons. The Select File button allows for users to choose a song file with a .wav extension to generate strum patterns for. The Play Song button plays the song and if the metronome is enabled, the metronome will play with it. The Pause Song button pauses the song and the metronome if enabled. The Restart Song button pauses and restarts the song and the metronome if enabled.
The Strum Pattern section has the Generate Strum Patterns button. This allows the user to see the strum pattern being used in the song currently. When the Play Song button is pressed in the Original Song section, the strum that is currently playing will be green. If the metronome strum mode is enabled the metronome will play a down-strum or up-strum noise with the strum.
The Metronome section has the Select Port, Enable Metronome, Disable Metronome, Strum Enable, and Strum Disable buttons. The Select Port button has a dialog box popup that has the user connect to the metronome serially using the port it is connected to. The Start button enables the metronome and the Stop button disables the metronome. The Strum Enable turns on strumming mode for the metronome which makes a noise for each strum when Generate Strum Patterns is on. The Strum Disable button turns off the strumming mode for the metronome.


        Navigation
There is only one screen with buttons that are well defined. There are minimal bugs.
Perception
There is only one screen with buttons that are well defined. Users should easily be able to understand what the buttons do and how to use them.
        Responsiveness
There are little to no delays in the build.


        Build Quality
        Robustness
There should be no crashes unless undefined behavior is done.
        Consistency
All buttons act predictably.
Detecting multiple strums and chords within the context of a song has proven to be a difficult signal processing problem and currently the outputs are inconsistent.  When using an audio file of a single strum and only trying to detect a single strum, the output is consistent.


        Aesthetic Rigor
The aesthetic does not interfere with the functionality of the project.


        Vertical Features
        External Interface
The GUI connects to a function that generates the strum pattern. This will be the persistent state when the strum pattern detection is finished. The GUI also connects to the metronome class which drives the metronome and sends commands to the microcontroller to tell the metronome what to do.


        Persistent State
The user can load a locally stored audio file in the GUI.  This will be passed to the internal signal processing systems and the external user interface as playable audio with a metronome and strum patterns.
The metronome class is used to drive the metronome. It sends predefined commands to control the metronome. This class is used by the GUI to interact with the metronome without sending any undefined functions for the microcontroller to do.
The persistent state will send a list of strums and their times back to the GUI once the strum detection is functioning. For now this is hardcoded.


        Internal Systems
The automatic detection of strum pattern and notes is still under development.  Currently if input with a wav file containing a single strum, the direction is determined by the slope of the time-frequency plane.  This needs to be expanded to the context of a song, the key being detecting the onset of notes or a new chord and looking at each in isolation.  Using the fundamental frequency method to detect the actual notes being played of the chord is also being developed.  This feature works to an extent, but additional notes not present in a chord are being read while some present are not.  Currently within the GUI the strum patterns are hard coded.
The metronome microcontroller code connects serially to the computer. It receives commands from the metronome class. The microcontroller interacts with the piezo to make a metronome and strumming sounds.