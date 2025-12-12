from midi2audio import FluidSynth

def midi_to_audio(midi_file: str, audio_file: str, soundfont: str = None):
    """
    Converts a MIDI file to an audio file using FluidSynth.

    Args:
        midi_file (str): Path to the input MIDI file.
        audio_file (str): Path to the output audio file (e.g., 'output.wav').
        soundfont (str, optional): Path to a soundfont file. If None, uses default.
    """
    fs = FluidSynth(sound_font=soundfont)
    fs.midi_to_audio(midi_file, audio_file)
    print(f"Audio file saved as {audio_file}")