from midi2audio import FluidSynth

# Specify your file paths and names
midi_file = "C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\5207.midi"
sound_font = "C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\sf2\\Yamaha_C7__Normalized_.sf2"
output_wav = "C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\5207.wav"

# Initialize FluidSynth with the specified sound font
fs = FluidSynth(sound_font)

# Convert the MIDI/MIDI file to WAV using the sound font
fs.midi_to_audio(midi_file, output_wav)

print(f"Conversion completed: {output_wav}")
