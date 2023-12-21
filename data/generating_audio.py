import pandas as pd
import os
import subprocess

# Define the function to convert MIDI to WAV using FluidSynth
def midi_to_wav(midi_path, wav_path, soundfont_path):
    command = f'fluidsynth -ni {soundfont_path} {midi_path} -F {wav_path} -r 44100'
    subprocess.run(command, shell=True)

# Load the dataset
df = pd.read_csv('data/updated_metadata_with_split.csv')

# Path to the MIDI files and soundfont
midi_folder = 'data/MIDI'
soundfont_path = 'path/to/your/soundfont.sf2'  # Update this with the actual path

# Create train, val, test folders
for folder in ['train', 'val', 'test']:
    os.makedirs(f'data/{folder}', exist_ok=True)

# Process files
for index, row in df.iterrows():
    if row['Split'] != 'excluded':
        file_number = row['File_Number']
        midi_file = f'{midi_folder}/{file_number}.mid'
        wav_file = f'data/{row["Split"]}/{file_number}.wav'

        # Convert MIDI to WAV
        midi_to_wav(midi_file, wav_file, soundfont_path)

        # Move MIDI file to the corresponding folder
        os.rename(midi_file, f'data/{row["Split"]}/{file_number}.mid')
