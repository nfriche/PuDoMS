import pandas as pd
import mido
import os

## Function to check if a MIDI file is monophonic
def is_monophonic(midifile):
    active_notes = set()
    ## Iterate through all messages in the MIDI file
    for msg in midifile:
        ## Check if the message is not a meta message (like tempo or time signature)
        if not msg.is_meta:
            ## Check that a note is being played
            if msg.type == 'note_on' and msg.velocity > 0:
                ## Identify whether or not more than one note is playing at a time
                if len(active_notes) >= 1:
                    return False
                active_notes.add(msg.note)
            ## Check is message is actually a note release and discard it if yes
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                active_notes.discard(msg.note)
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
        ## Check data types and values
        print(f"Processing file: {file}, File Number: {file_number}")
        if is_monophonic(mid):
            print(f"File {file_number} is Monophonic")
            merged_df.loc[merged_df['File_Number'] == file_number, 'Monophonic'] = 'Yes'
        else:
            print(f"File {file_number} is Not Monophonic")
            merged_df.loc[merged_df['File_Number'] == file_number, 'Monophonic'] = 'No'

## Save the updated dataframe to metadata.csv
merged_df.to_csv('metadata.csv', index=False)

## Display the first few rows of the merged dataframe
print(merged_df.head())
