import os
import shutil 
import pandas as pd
from midi2audio import FluidSynth

# Paths
midi_folder = "MIDI"
sf2_folder = "sf2"
sf2_file = os.path.join(sf2_folder, "Steinway_Model_D274.sf2")
metadata_file = "pudoms.csv"
output_folder = "PuDoMS"  # New folder for audio and copied MIDI files

# Ensure the MIDI and output folders exist
os.makedirs(midi_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)  # Create the output folder

# Initialize FluidSynth for MIDI to WAV conversion
fs = FluidSynth(sf2_file)

# Read metadata
metadata = pd.read_csv(metadata_file)

# Process each file
for index, row in metadata.iterrows():
    try:
        # Check both possible file extensions
        midi_file = f"{row['File_Number']}.midi"
        original_path = os.path.join(midi_folder, midi_file)
        if not os.path.exists(original_path):
            midi_file = f"{row['File_Number']}.mid"  # Check for .mid file
            original_path = os.path.join(midi_folder, midi_file)

        # Define path for the WAV file in the output folder
        wav_path = os.path.join(output_folder, f"{row['File_Number']}.wav")

        # Optionally, copy the MIDI file to the output folder
        midi_copy_path = os.path.join(output_folder, midi_file)
        if os.path.exists(original_path) and not os.path.exists(midi_copy_path):
            shutil.copy2(original_path, midi_copy_path)

        # Skip conversion if WAV file already exists in the output folder
        if os.path.exists(wav_path):
            print(f"WAV file for {midi_file} already exists in {output_folder}. Skipping conversion.")
            continue

        # Check if the MIDI file exists
        if os.path.exists(original_path):
            # Convert MIDI to WAV and save in the output folder
            fs.midi_to_audio(original_path, wav_path)
            print(f"Converted {midi_file} to WAV and saved in {output_folder}.")
        else:
            print(f"File {midi_file} does not exist. Skipping...")
    except Exception as e:
        print(f"Error processing file number: {row['File_Number']}. Error: {e}")

print("Conversion and organization completed.")

