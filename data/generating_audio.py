import os
import pandas as pd
from midi2audio import FluidSynth
import subprocess  # to call git commands

# Function to push files to git
def push_to_git(commit_message):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while pushing files to git:", str(e))

# Paths and initialization
midi_folder = "MIDI"
sf2_folder = "C:\\Users\\nikit\\escraping_hell\\sf2"
sf2_file = os.path.join(sf2_folder, "Clean_Concert_Grand.sf2")  
metadata_file = "updated_metadata_with_split.csv"
metadata = pd.read_csv(metadata_file)
fs = FluidSynth(sf2_file)

# Batch settings
batch_size = 50  
current_batch = 0

# Create folders if they don't exist
for folder in ["train", "validation", "test"]:
    os.makedirs(folder, exist_ok=True)

# Process each file
for index, row in metadata.iterrows():
    try:
        midi_file = f"{row['File_Number']}.midi"
        original_path = os.path.join(midi_folder, midi_file)
        if not os.path.exists(original_path):
            midi_file = f"{row['File_Number']}.mid"
            original_path = os.path.join(midi_folder, midi_file)

        if os.path.exists(original_path) and row['Split'] in ['train', 'validation', 'test']:
            new_path = os.path.join(row['Split'], midi_file)
            os.rename(original_path, new_path)
            wav_file = f"{row['File_Number']}.wav"
            wav_path = os.path.join(row['Split'], wav_file)
            fs.midi_to_audio(new_path, wav_path)

            current_batch += 1
            if current_batch >= batch_size:
                push_to_git(f"Adding batch of WAV files - {index}")
                current_batch = 0  # reset the batch count after pushing
    except Exception as e:
        print(f"Error processing file number: {row['File_Number']}. Error: {e}")

# Push any remaining files at the end
if current_batch > 0:
    push_to_git("Adding final batch of WAV files")

print("Conversion and organization completed.")

