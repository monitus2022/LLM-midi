import json
from mido import Message, MidiFile, MidiTrack, MetaMessage

# ---- Config ----
PPQ = 480            # pulses per quarter note
BEATS_PER_BAR = 4
TEMPO_BPM = 150      # optional; adjust if needed

# Map duration tags to ticks
DUR_MAP = {
    "16": PPQ // 4,
    "8": PPQ // 2,
    "q": PPQ,
    "h": PPQ * 2,
    "w": PPQ * 4,
    "d16": int(PPQ // 4 * 1.5),
    "d8": int(PPQ // 2 * 1.5),
    "d4": int(PPQ * 1.5),
    "d2": int(PPQ * 2 * 1.5),
}

# Note name to MIDI number (C4 = 60, A4 = 69)
SEMITONES = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "Fb": 4, "E#": 5,  # optional enharmonics
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11, "Cb": 11, "B#": 0, # B# ~ C
}

def note_to_midi(note_str: str) -> int:
    # e.g., "Eb5", "C#4", "G4"
    # split letter+accidental from octave
    i = 1
    if len(note_str) >= 2 and note_str[1] in ("#", "b"):
        i = 2
    name = note_str[:i]
    octave = int(note_str[i:])
    semitone = SEMITONES[name]
    # MIDI formula: note_number = (octave + 1) * 12 + semitone
    return (octave + 1) * 12 + semitone

def dur_to_ticks(d: str) -> int:
    if d not in DUR_MAP:
        raise ValueError(f"Unknown duration tag: {d}")
    return DUR_MAP[d]

def bpm_to_tempo(bpm: int) -> int:
    # microseconds per beat
    return int(60_000_000 / bpm)

def event_start_ticks(bar: int, t: float) -> int:
    # t is beat position within the bar (1-based: 1..4, can be fractional)
    total_beats_before_bar = (bar - 1) * BEATS_PER_BAR
    beat_offset_in_bar = (t - 1.0)
    total_beats = total_beats_before_bar + beat_offset_in_bar + 1.0 - 1.0  # normalize
    # Since t is already absolute within bar (1-based), simpler:
    return ((bar - 1) * BEATS_PER_BAR + (t - 1.0)) * PPQ

def build_messages(midi_events):
    # Create absolute-time note_on/off messages
    msgs = []
    for ev in midi_events:
        bar = ev["bar"]
        t = ev["t"]
        note = note_to_midi(ev["note"])
        vel = ev["vel"]
        dur_ticks = dur_to_ticks(ev["dur"])
        start = int(event_start_ticks(bar, t))
        end = start + dur_ticks
        # note_on at start, note_off at end
        msgs.append(("note_on", start, note, vel))
        msgs.append(("note_off", end, note, 0))
    # Sort by absolute tick, note_off after note_on if same tick
    msgs.sort(key=lambda m: (m[1], 0 if m[0] == "note_on" else 1))
    # Convert to delta times
    delta_msgs = []
    last_tick = 0
    for typ, tick, note, vel in msgs:
        delta = tick - last_tick
        delta_msgs.append((typ, note, vel, delta))
        last_tick = tick
    return delta_msgs

def json_to_midi(json_path: str, out_mid: str):
    with open(json_path, "r") as f:
        data = json.load(f)

    mid = MidiFile(ticks_per_beat=PPQ)
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo
    track.append(MetaMessage("set_tempo", tempo=bpm_to_tempo(TEMPO_BPM), time=0))
    # Optional: set instrument (program change) on channel 0
    # track.append(Message("program_change", program=80, time=0))  # e.g., lead

    # Flatten events
    flat = data["midi"]  # list of dicts with bar,t,note,dur,vel
    delta_msgs = build_messages(flat)

    # Write messages
    for typ, note, vel, delta in delta_msgs:
        track.append(Message(typ, note=note, velocity=vel, time=delta, channel=0))

    mid.save(out_mid)

if __name__ == "__main__":
    json_to_midi("../output/midi_spec.json", "../output/melody.mid")
    print("Wrote melody.mid")
