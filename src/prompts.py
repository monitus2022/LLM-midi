DEFINE_MUSIC_PLAN_PROMPT = """
You are a music composer planning a piece before writing notes. 
Given a text description (e.g., "retro 8-bit battle theme"), create a structured outline of the music. 
Your output must include ALL of the following categories, in numbered order:

1. Genre/style: Specify the musical genre and stylistic influences, with references if relevant.
2. Mood/emotion: Describe the emotional character and atmosphere.
3. Tempo/feel: Give approximate BPM, meter (e.g., 4/4), and rhythmic feel.
4. Key signature & tonality: State the key (e.g., C minor) and whether it is major/minor/modal.
5. Instrumentation palette: List exactly 4 instruments/timbres, each with its role (melody, bass, percussion, harmony/pad).
6. Sectional structure: Break the piece into sections (intro, A, B, bridge, outro), with bar counts and transitions.
7. Motivic ideas: Describe recurring melodic or rhythmic motifs for each section.
8. Dynamic contour: Explain how intensity rises and falls across sections.
9. Length/scale: Approximate total bars and duration at the given tempo.
10. Looping behavior: State whether the piece loops, and if so, from which section.

Format the answer as a numbered list with concise but specific details. 
Do not generate notes or MIDI tokens yet—only the high-level outline.
"""

DEFINE_CHORD_RHYTHM_PROMPT = """
You are a music arranger expanding a structured outline into harmonic and rhythmic detail. 
Given the outline below, generate chord progressions and rhythm grids for each section.

Outline:
{music_plan}

Your output must include:

Your output must include ALL of the following:


Your output must include ALL of the following:

1. Key signature & tonality confirmation.

2. For each section (Intro, A, B, Bridge, A’, Outro):
   - Chord progression: list chords bar by bar.
   - Rhythm grid: describe bass, percussion, melody, and harmony per bar.
   - Motif integration: specify motifs and the exact bars they appear.
   - Percussion variation: include fills, rolls, or transitions per section.
   - Voice leading cues: describe how melody moves between chords (stepwise, leaps, octave shifts).
   - Dynamics: add bar-level markings (e.g., crescendo in bar 7, accent in bar 8).
   - Polyphony limits: enforce max 2 voices per channel (NES-style).
   - Looping consideration: describe how the section transitions back or forward.

3. Format the answer as a structured list, section by section, with chords and rhythm grids clearly separated. 
Do not generate MIDI tokens yet—only harmonic and rhythmic plans.
"""

NOTE_EVENTS_PROMPT = """
You are a symbolic music generator. 
Given the following harmonic and rhythmic plan, output structured note events suitable for MIDI conversion.

Plan:
[Paste Section Breakdown from Prompt 2 here]

Your output must include:

1. Note events in the format:
   [bar, beat, channel, pitch, duration, velocity]

   - bar: integer (1–N)
   - beat: subdivision (e.g., 1, 1.5 for "and of 1")
   - channel: instrument assignment
       - Channel 1 = Square wave (melody)
       - Channel 2 = Pulse wave (bass)
       - Channel 3 = Noise channel (percussion)
       - Channel 4 = Triangle wave (harmony/pad)
   - pitch: note name with octave (e.g., E4, G#3), or "PercKick", "PercSnare", "PercHat" for noise events
   - duration: rhythmic value (e.g., quarter, 8th, 16th, whole)
   - velocity: 0–127 (approximate dynamics)

2. Respect NES-style polyphony limits:
   - Max 2 voices per channel at any time.

3. Place motifs exactly where specified in the plan:
   - Motif A = descending 4ths (A–E–B)
   - Motif B = rising arpeggio (E–G–B–D)
   - Motif C = chromatic descent (B–A–G#–G)
   - Motif D = descending scale (B–A–G–F#)

4. Dynamics: reflect crescendos/decrescendos by adjusting velocity values.

5. Percussion mapping:
   - Kick = PercKick
   - Snare = PercSnare
   - Hi-hat = PercHat
   - Fills/rolls = repeated PercSnare or PercHat with shorter durations.

6. Output section by section, bar by bar, with clear separation.

Do not describe or explain—only output structured note events.
"""