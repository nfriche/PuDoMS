import mido
import os
import csv

def is_monophonic(midifile, overlap_threshold=10):  # overlap_threshold in milliseconds
    if len(midifile.tracks) != 1:  # Check if the MIDI file has only one track
        return False

    active_notes = set()
    last_note_on_time = -1
    current_time = 0  # Initialize current time to track the timing of messages

    for msg in midifile.tracks[0]:  # Iterate over messages in the single track
        if not msg.is_meta and msg.time is not None:  # Check if the message is not a meta message and has time information
            current_time += msg.time  # Update the current time with the delta time of the message
            if msg.type == 'note_on' and msg.velocity > 0:  # Check for 'note_on' message with a velocity greater than 0 (indicating note start)
                if len(active_notes) >= 1:  # Check if there is already another note playing
                    # If the new note starts within the allowed overlap threshold, consider it polyphonic
                    if (current_time - last_note_on_time) <= overlap_threshold:
                        return False
                active_notes.add(msg.note)  # Add the note to the set of active notes
                last_note_on_time = current_time  # Update the last note-on time
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):  # Check for 'note_off' message or 'note_on' with velocity 0 (indicating note end)
                active_notes.discard(msg.note)  # Remove the note from the set of active notes

    # If no notes were found in the file (i.e., active_notes is empty and last_note_on_time is unchanged)
    if len(active_notes) == 0 and last_note_on_time == -1:
        return None  # Return None or handle as you see fit (indicating an empty track)

    # If the function hasn't returned False by now, the file is considered monophonic
    return True  

def find_monophonic_midis(folder_path):
    monophonic_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".mid") or file.endswith(".midi"):
            path = os.path.join(folder_path, file)
            mid = mido.MidiFile(path)
            # Check if file is monophonic
            if is_monophonic(mid):
                # Store number only 
                number = file.split('.')[0]
                monophonic_files.append(number)
    return monophonic_files

def write_to_csv(file_list, csv_file_name):
    with open(csv_file_name, mode='w', newline='') as file:
        fieldnames = ['File_Number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  
        for name in file_list:
            writer.writerow({'File_Number': name})  

midi_folder_path = 'C:\\Users\\nikit\\escraping_hell\\MIDI'
monophonic_files = find_monophonic_midis(midi_folder_path)

# Write the numbers of monophonic MIDI files to a CSV file
write_to_csv(monophonic_files, 'monophonic_midi_numbers.csv')
