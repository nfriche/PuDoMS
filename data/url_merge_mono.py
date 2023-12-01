import pandas as pd
import mido
import os

## Function to check if a MIDI file is monophonic
def is_monophonic(midifile):
    ## Iterate through each track in the MIDI file
    for track in midifile.tracks:
        ## Initialize a set to keep track of active notes
        active_notes = set()
        ## Iterate through all messages in the track
        for msg in track:
            ## Check if the message is not a meta message (like tempo or time signature)
            if not msg.is_meta:
                ## Check if the message is a note being played (note_on with velocity > 0)
                if msg.type == 'note_on' and msg.velocity > 0:
                    ## Check if there is already a note playing (set length >= 1)
                    ## If so, return False as this means multiple notes are playing
                    if len(active_notes) >= 1:
                        return False
                    ## Add the note to the set of active notes
                    active_notes.add(msg.note)
                ## Check if the message is a note release (note_off) or note_on with velocity 0
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    ## Remove the note from the set of active notes
                    active_notes.discard(msg.note)
    ## If the function hasn't returned False, it means no polyphony was detected, return True
    return True

## Load the CSV files
urls_df = pd.read_csv('urls.csv')
metadata_df = pd.read_csv('metadata.csv')

## Append the URL column from urls_df to metadata_df
merged_df = pd.concat([metadata_df, urls_df['URL']], axis=1)

## Directory containing MIDI files
midi_folder_path = 'C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\MIDI'

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
