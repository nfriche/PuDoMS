import os
import librosa

# Define the folder containing your WAV files
wav_folder = "validation"

# Iterate over each file in the directory
for filename in os.listdir(wav_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(wav_folder, filename)

        # Load the audio file
        y, sr = librosa.load(file_path, sr=None)

        # Calculate the root mean square (RMS) energy for each frame of audio
        # RMS close to 0 indicates silence
        rms = librosa.feature.rms(y=y)[0]

        # Check if the RMS is below a threshold, indicating silence
        if max(rms) < 0.01:  # You might need to adjust this threshold
            print(f"{filename} is silent.")
