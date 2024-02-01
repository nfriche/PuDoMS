import os
import mido

def count_notes_in_midi(file_path):
    """ Count the number of notes in a single MIDI file. """
    midi = mido.MidiFile(file_path)
    note_count = 0
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note_count += 1
    return note_count

def count_notes_in_directory(directory):
    """ Count the total number of notes in all MIDI files in a directory. """
    total_notes = 0
    for file in os.listdir(directory):
        if file.endswith('.mid') or file.endswith('.midi'):
            file_path = os.path.join(directory, file)
            total_notes += count_notes_in_midi(file_path)

    return total_notes

midi_folder_path = "C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\MIDI"
total_notes = count_notes_in_directory(midi_folder_path)
print(f"Total number of notes in all MIDI files: {total_notes}")
