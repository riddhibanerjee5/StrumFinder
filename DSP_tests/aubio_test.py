import aubio
import numpy as np

# Load audio file
source = aubio.source("pigstrum.wav")
sr = source.samplerate

# Create pitch detection object
pitch_o = aubio.pitch("yin", sr)

# Set unit (Hz or midi)
pitch_o.set_unit("Hz")

# Set tolerance
pitch_o.set_tolerance(0.8)

# Initialize an empty array to store the pitches
pitches = []

# Initialize an empty array to store the confidence of the pitches
confidences = []

# Process audio file
while True:
    samples, read = source()
    if read < source.hop_size:
        break
    pitch = pitch_o(samples)[0]
    pitches.append(pitch)
    confidences.append(pitch_o.get_confidence())

# Compute the pitch difference between consecutive frames
d_pitch = np.diff(pitches)

# Threshold for detecting pitch changes
threshold = 5

# Initialize an empty array to store the frames where the pitch difference is greater than the threshold
upstrum_frames = []

# Iterate through the frames of the pitch difference
for i in range(d_pitch.shape[0]):
    # Check if the pitch difference in the frame is greater than the threshold
    if d_pitch[i] > threshold:
        # If so, add the frame index to the list of upstrum frames
        upstrum_frames.append(i)

# Check if the upstrum frames are found at the attack of the notes
if upstrum_frames[0] < 20:
    print("Guitar is upstrummed")
else:
    print("Guitar is downstrummed")