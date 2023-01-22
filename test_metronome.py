from metronome import metronome
from time import sleep

metro = metronome()
metro.set_serial("COM3")
metro.set_bpm(120)
metro.play()
sleep(3)
metro.pause()
sleep(1)
print("resume")
metro.unpause(120, 1200)
sleep(3)
metro.pause()