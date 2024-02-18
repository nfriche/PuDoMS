import mido
import os

def merge_midi_tracks(input_file_path, output_file_path):
    """
    Merges all tracks of a MIDI file into a single track, preserving notes,
    tempo changes, and time signatures, and handling overlapping notes.

    :param input_file_path: Path to the input MIDI file.
    :param output_file_path: Path where the processed MIDI file will be saved.
    """
    # Load the MIDI file
    mid = mido.MidiFile(input_file_path)
    # Prepare a list to hold all messages with their absolute time
    messages = []
    current_time = 0
    # Extract messages from all tracks, keeping their time in absolute form
    for track in mid.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            messages.append(msg.copy(time=current_time))
    # Sort messages by their absolute time
    messages.sort(key=lambda msg: msg.time)
    # Track the state of each note
    note_states = {}
    # Process messages to handle overlapping notes
    processed_messages = []
    for msg in messages:
        if msg.type == 'note_on' and msg.velocity > 0:
            note = msg.note
            if note_states.get(note, False):  # If note is already on, add a note off
                processed_messages.append(mido.Message('note_off', note=note, velocity=0, time=msg.time))
            note_states[note] = True  # Mark note as on
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            note = msg.note
            if note_states.get(note, False):  # If note is on, mark it as off
                note_states[note] = False
            else:
                continue  # Skip this note off if the note was not on
        processed_messages.append(msg)
    # Create a new MIDI file with the merged track
    merged_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat)
    merged_track = mido.MidiTrack()
    merged_mid.tracks.append(merged_track)
    # Convert absolute times back to delta times and add to the merged track
    last_time = 0
    for msg in processed_messages:
        delta_time = msg.time - last_time
        last_time = msg.time
        msg.time = delta_time
        merged_track.append(msg)
    # Save the new MIDI file
    merged_mid.save(output_file_path)


def process_folder(input_folder, output_folder):
    """
    Processes all MIDI files in the input folder, merging their tracks,
    and saves them into the output folder.

    :param input_folder: Path to the folder containing MIDI files.
    :param output_folder: Path where processed MIDI files will be saved.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # List all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a MIDI file
        if filename.endswith('.midi') or filename.endswith('.mid'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            print(f"Processing {filename}...")
            merge_midi_tracks(input_file_path, output_file_path)
            print(f"Saved processed file to {output_file_path}")


input_folder = 'MIDI'
output_folder = 'PuDoMS'
process_folder(input_folder, output_folder)
