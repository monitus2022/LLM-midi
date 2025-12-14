from midi2audio import FluidSynth

def synthesize_audio(midi_path, audio_path, soundfont_path='soundfonts/FluidR3_GM.sf2'):
    """
    Synthesize audio from a MIDI file using FluidSynth.

    Args:
        midi_path (str): Path to the input MIDI file.
        audio_path (str): Path to the output audio file (e.g., .wav).
        soundfont_path (str): Path to the soundfont file.
    """
    fs = FluidSynth(soundfont_path)
    fs.midi_to_audio(midi_path, audio_path)

if __name__ == "__main__":
    synthesize_audio(
        '../output/generated_music.mid', 
        '../output/generated_music.wav',
        '../soundfonts/8bit.sf2'
        )