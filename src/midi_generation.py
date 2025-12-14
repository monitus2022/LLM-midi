import json
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage


def json_to_midi(json_path, output_path='output.mid', bpm=150, ticks_per_beat=480):
    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Create MIDI file
    mid = MidiFile(ticks_per_beat=ticks_per_beat)

    # Set tempo
    tempo = mido.bpm2tempo(bpm)

    # Channel mappings
    channel_map = {
        'melody': 0,
        'bass': 1,
        'harmony': 2,
        'perc': 9  # Drum channel
    }

    # Drum note mappings
    drum_notes = {
        'Kick': 36,
        'Snare': 38,
        'HiHat': 42,
        'Noise': 39
    }

    # Duration mappings (in beats)
    duration_map = {
        'thirtysecond': 0.125,
        'thirty-second': 0.125,
        'sixteenth': 0.25,
        'eighth': 0.5,
        'quarter': 1.0,
        'half': 2.0,
        'whole': 4.0
    }

    note_names = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
                  'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}

    # Function to convert pitch to MIDI note
    def pitch_to_midi(pitch_str):
        if pitch_str in drum_notes:
            return drum_notes[pitch_str]
        # Parse note like "D4" -> D in octave 4
        note = ''.join([c for c in pitch_str if not c.isdigit()])
        octave = int(''.join([c for c in pitch_str if c.isdigit()]))
        return note_names[note] + (octave + 1) * 12

    # Process each channel
    for channel_name in ['melody', 'bass', 'harmony', 'perc']:
        if channel_name not in data:
            continue
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        track.append(Message('program_change', program=0,
                     channel=channel_map[channel_name], time=0))

        # Get sections
        if channel_name in ['melody', 'harmony']:
            sections = data[channel_name]['sections']
        else:
            sections = data[channel_name]

        # Limit perc volumne
        if channel_name == 'perc':
            for section in sections:
                for bar in section['bars']:
                    for i, event in enumerate(bar['events']):
                        beat, pitch, dur, vel = event
                        vel = min(vel, 80)  # Limit velocity
                        bar['events'][i] = (beat, pitch, dur, vel)

        # Collect all events with absolute time
        events = []
        bar_offset = 0
        for section in sections:
            for bar in section['bars']:
                bar_num = bar['bar']
                for event in bar['events']:
                    beat, pitch, dur, vel = event
                    start_time = (bar_offset + bar_num - 1) * \
                        4 + beat  # 4 beats per bar
                    duration_beats = duration_map[dur]
                    end_time = start_time + duration_beats
                    midi_note = pitch_to_midi(pitch)
                    events.append(('note_on', midi_note, vel, start_time))
                    events.append(('note_off', midi_note, 0, end_time))
            # Assuming bars are sequential per section
            bar_offset += len(section['bars'])

        # Sort events by time
        events.sort(key=lambda x: x[3])

        # Add to track with deltas
        last_time = 0
        for event_type, note, vel, time in events:
            delta = int((time - last_time) * ticks_per_beat)
            track.append(Message(event_type, note=note, velocity=vel,
                         channel=channel_map[channel_name], time=delta))
            last_time = time

    # Save MIDI file
    mid.save(output_path)


if __name__ == "__main__":
    json_to_midi('../output/note_events.json',
                 output_path='../output/generated_music.mid', bpm=150)
