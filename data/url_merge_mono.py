import pandas as pd
import mido
import os

## Function to check if a MIDI file is monophonic
def is_monophonic(midifile):
    ## Iterate through each track in the MIDI file
    for track in midifile.tracks:
        ## Track the number of notes playing at a time
        notes_playing = 0
        ## Iterate through all messages in the track
        for msg in track:
            ## Check if the message is a note on and velocity > 0 (note start)
            if msg.type == 'note_on' and msg.velocity > 0:
                notes_playing += 1
                ## If more than one note is playing, it's not monophonic
                if notes_playing > 1:
                    return False
            ## Check if the message is a note off or note on with velocity 0 (note end)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                notes_playing = max(0, notes_playing - 1)
    ## If the track has no polyphony, it's monophonic
    return True

## Load the CSV files
urls_df = pd.read_csv('urls.csv')
metadata_df = pd.read_csv('metadata.csv')

## Append the URL column from urls_df to metadata_df
merged_df = pd.concat([metadata_df, urls_df['URL']], axis=1)

## Directory containing MIDI files
midi_folder_path = 'path_to_your_midi_files'  # Update this to your MIDI files folder path

## Add a 'Monophonic' column with default value 'No'
merged_df['Monophonic'] = 'No'

## Check each MIDI file and update the 'Monophonic' column
for file in os.listdir(midi_folder_path):
    if file.endswith(".mid") or file.endswith(".midi"):
        path = os.path.join(midi_folder_path, file)
        mid = mido.MidiFile(path)
        file_number = file.split('.')[0]
        ## Check if file is monophonic and update the dataframe
        if is_monophonic(mid):
            ## Update the 'Monophonic' column based on the File_Number
            merged_df.loc[merged_df['File_Number'] == file_number, 'Monophonic'] = 'Yes'
        else:
            ## If the file is not monophonic, ensure it's marked 'No'
            merged_df.loc[merged_df['File_Number'] == file_number, 'Monophonic'] = 'No'

## Save the updated dataframe to metadata.csv
merged_df.to_csv('metadata.csv', index=False)

## Display the first few rows of the merged dataframe
print(merged_df.head())
