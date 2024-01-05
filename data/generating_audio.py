import os
import pandas as pd
from midi2audio import FluidSynth

# Paths
midi_folder = "MIDI"
sf2_folder = "sf2"
sf2_file = os.path.join(sf2_folder, "Clean_Concert_Grand.sf2")  
metadata_file = "updated_metadata_with_split.csv"

# Read metadata
metadata = pd.read_csv(metadata_file)

# Create folders if they don't exist
for folder in ["train", "validation", "test"]:
    os.makedirs(folder, exist_ok=True)

# Initialize FluidSynth for MIDI to WAV conversion
fs = FluidSynth(sf2_file)

# Process each file
for index, row in metadata.iterrows():
    try:
        # Check both possible file extensions
        midi_file = f"{row['File_Number']}.midi"
        original_path = os.path.join(midi_folder, midi_file)
        if not os.path.exists(original_path):
            # If .midi file doesn't exist, check for .mid file
            midi_file = f"{row['File_Number']}.mid"
            original_path = os.path.join(midi_folder, midi_file)

        # Check if the file exists and is not excluded
        if os.path.exists(original_path) and row['Split'] in ['train', 'validation', 'test']:
            # Define new path
            new_path = os.path.join(row['Split'], midi_file)
            
            # Move MIDI file to the corresponding folder
            os.rename(original_path, new_path)
            print(f"Moved {midi_file} to {row['Split']} folder.")
            
            # Convert and save WAV file
            wav_file = f"{row['File_Number']}.wav"
            wav_path = os.path.join(row['Split'], wav_file)
            fs.midi_to_audio(new_path, wav_path)
            print(f"Converted {midi_file} to WAV and moved to {row['Split']} folder.")
        else:
            print(f"File {midi_file} does not exist or is excluded. Skipping...")

    except Exception as e:
        print(f"Error processing file number: {row['File_Number']}. Error: {e}")

print("Conversion and organization completed.")
