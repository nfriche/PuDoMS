import mido
import os

def contains_piano(midifile):
    for track in midifile.tracks:
        for msg in track:
            if msg.type == 'program_change':
                # General MIDI piano program numbers are 0-7 (1-8 in MIDI standard)
                if 0 <= msg.program <= 7:
                    return True
    return False

def check_midi_files_for_piano(folder_path):
    no_piano_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".mid") or file.endswith(".midi"):
            path = os.path.join(folder_path, file)
            mid = mido.MidiFile(path)
            if not contains_piano(mid):
                no_piano_files.append(file)
    return no_piano_files

# Use the provided path
midi_folder_path = 'C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\MIDI'
files_without_piano = check_midi_files_for_piano(midi_folder_path)

if files_without_piano:
    print("Files without piano:", files_without_piano)
else:
    print("All files contain piano.")
