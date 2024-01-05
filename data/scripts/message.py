import mido

# Load the original MIDI file
midi_file_path = "C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\train\\5207.midi"
mid = mido.MidiFile(midi_file_path)

# Create a new MIDI file object to hold the modified data
new_mid = mido.MidiFile()

for track in mid.tracks:
    new_track = mido.MidiTrack()
    for msg in track:
        # If the message is a control change on channel 0 with control number 121, skip it
        if msg.type == 'control_change' and msg.control == 121 and msg.channel == 0:
            continue  # Skip adding this message to the new track
        else:
            # Otherwise, add the message as-is to the new track
            new_track.append(msg)
    new_mid.tracks.append(new_track)  # Add the modified track to the new MIDI file

# Save the new MIDI file
new_midi_file_path = "C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\5207.midi"
new_mid.save(new_midi_file_path)

print(f"Modified MIDI file saved as {new_midi_file_path}")
