# StrumFinder

Build Instructions:
  python main.py

STFT Note: 
The stft.cpp file correctly takes the Short Time Fourier Transform of an input array (sample values from audio file).
This was tested in Visual Studio 2019, feel free to try in any IDE.  The chirp.txt file can be used to take the STFT of a chirp sound.
The STFT is very useful because it takes Fourier transforms at specified intervals of time over the sample data, allowing one to view the frequency domain of these intervals and deduce musical notes.
