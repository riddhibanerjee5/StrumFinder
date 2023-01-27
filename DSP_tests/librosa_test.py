import librosa
import numpy as np

# Load audio file
y, sr = librosa.load("riptide.wav")

# Compute the STFT
stft = librosa.core.stft(y)

# Compute the phase of the STFT
phase = np.angle(stft)

# Compute the phase difference between consecutive frames
d_phase = np.diff(phase, axis=1)

# Threshold for detecting phase changes
threshold = 0.2

# Initialize an empty array to store the frames where the phase difference is greater than the threshold
upstrum_frames = []

# Iterate through the frames of the phase difference
for i in range(d_phase.shape[1]):
    # Check if the maximum phase difference in the frame is greater than the threshold
    if np.max(np.abs(d_phase[:, i])) > threshold:
        # If so, add the frame index to the list of upstrum frames
        upstrum_frames.append(i)

# Check if the upstrum frames are found at the attack of the notes
if upstrum_frames[0] < 20:
    print("Guitar is upstrummed")
else:
    print("Guitar is downstrummed")
