import mido
import os
import csv

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

def find_monophonic_midis(folder_path):
    monophonic_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".mid") or file.endswith(".midi"):
            path = os.path.join(folder_path, file)
            mid = mido.MidiFile(path)
            ## Check if file is monophonic
            if is_monophonic(mid):
                ## Store number only 
                number = file.split('.')[0]
                monophonic_files.append(number)
    return monophonic_files

def write_to_csv(file_list, csv_file_name):
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for name in file_list:
            writer.writerow([name])

## Replace your_midi_folder_path with the path to your MIDI folder
midi_folder_path = 'your_midi_folder_path'
monophonic_files = find_monophonic_midis(midi_folder_path)

## Write the numbers of monophonic MIDI files to a CSV file
write_to_csv(monophonic_files, 'monophonic_midi_numbers.csv')
