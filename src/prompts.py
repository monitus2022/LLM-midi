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


DEFINE_CHORD_PROMPT = """
You are a music arranger. 
Given the outline below, output only the harmonic backbone in compact JSON.

Output format:
{
  "key": "D minor (Dorian inflections)",
  "sections": [
    {
      "name": "Intro",
      "bars": 4,
      "chords": ["Dm","Dm(add9)/F","Bb","F/C"],
      "motifs": {"Intro":[1,2,3,4]},
      "loop": "cut to A"
    },
    {
      "name": "A",
      "bars": 8,
      "chords": ["Dm","Bb","F","C","Dm","Gm","Am","Dm"],
      "motifs": {"A":[5,6,7,8,9,10,11,12]},
      "loop": "repeat or to B"
    }

  ]
}
Do not include rhythm grids, dynamics, or other details yet.

Outline:

"""


DEFINE_RHYTHM_PROMPT = """
You are a music arranger. 
Given the harmonic backbone below, expand into rhythmic and expressive detail in compact JSON.

Output format:
{
  "section": "A",
  "bars": 8,
  "bass": ["8ths root-5th bars 1-6","sync 16ths bars 7-8"],
  "perc": ["KickSnareHat default","snare fill bar 8"],
  "melody": ["Motif A bars 1-2,5-6","Motif B bars 3-4,7-8"],
  "harmony": ["sustain triads","crescendo bar 7"],
  "voiceLeading": ["stepwise in B","leaps in A"],
  "dynamics": ["mf bars 1-4","crescendo bar 7","f bar 8"],
  "polyphony": "≤2 voices/channel",
  "loop": "resolves to Em, repeat or transition to B"
}
Do not regenerate chords—only add rhythmic/expression detail.

Backbone:

"""


NOTE_EVENTS_PROMPT = """
You are a symbolic music generator.
Given the harmonic + rhythmic plan, output structured note events in JSON.
Only include the __CHANNEL__ channel. Do not include other channels.

Output format:
{
  "section": "Intro",
  "bars": [
    {
      "bar": 1,
      "events": [
        [1, "D4", "quarter", 80],
        [2, "F4", "eighth", 85],
        [2.5, "A4", "eighth", 85],
        [1, "D2", "quarter", 90],
        [1, "PercKick", "quarter", 100]
      ]
    },
    {
      "bar": 2,
      "events": [...]
    }
  ]
}

In the example, the first element in "events" represent the following:
{"beat":1, "pitch":"D4", "dur":"quarter", "vel":80}

Input:

"""


ALL_CHANNELS = ["melody", "bass", "perc", "harmony"]
