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


# NOTE_EVENTS_PROMPT = """
# You are a symbolic music generator.
# Given the harmonic + rhythmic plan, output structured note events in JSON.

# Output format:
# {
#   "section": "Intro",
#   "bars": [
#     {
#       "bar": 1,
#       "events": [
#         [1, "melody", "D4", "quarter", 80],
#         [2, "melody", "F4", "eighth", 85],
#         [2.5, "melody", "A4", "eighth", 85],
#         [1, "bass", "D2", "quarter", 90],
#         [1, "perc", "PercKick", "quarter", 100]
#       ]
#     },
#     {
#       "bar": 2,
#       "events": [...]
#     }
#   ]
# }

# The elements in "events" represent the following:
# {"beat":1,"channel":"melody","pitch":"D4","dur":"quarter","vel":80}
# Do not include bass, percussion, or harmony events—only melody.

# Input:

# """

NOTE_EVENTS_PROMPT = {
    "melody": """
      You are a symbolic music generator. 
      Generate melody note events in compact JSON. 
      Do not include bass, percussion, or harmony.

      Output rules:
      1. Use JSON only, no prose.
      2. Global bar numbering must continue across sections (Intro=1–4, A=5–12, B=13–20, etc.).
      3. Each section is an object: {"section":"A","bars":[...]}.
      4. Each bar must be a JSON object with one of two forms:
         - Expanded events:
         {"bar":5,"events":[{"t":1,"p":"D4","d":"16","v":80},{"t":1.25,"p":"F4","d":"16","v":80}]}
         - Motif shorthand:
         {"bar":9,"motif":"A","pattern":"chiptune_run","vel":100}
      5. Do not mix schemas inside the same bar. Every bar must have either "events" or "motif".
      6. Keys must be short:
         - t = beat (numeric, e.g. 1, 1.25, 2)
         - p = pitch (note+octave, e.g. "A4")
         - d = duration ("16","8","q","h","w","d8","d4")
         - v = velocity (0–127)
         - motif = motif ID (A–D) if used
         - pattern = shorthand description of rhythm/ornament
      7. Use motif references whenever possible instead of spelling out repeated notes.
      8. ≤2 voices per channel at once.
      9. No commentary, only valid JSON.

      Output format example:
      {
      "section":"Intro",
      "bars":[
         {"bar":1,"events":[{"t":1,"p":"D4","d":"q","v":80},{"t":2,"p":"E4","d":"8","v":85}]},
         {"bar":2,"motif":"Intro","pattern":"chromatic_rise","vel":85}
      ]
      }

      Input:

      """,
    "bass": """
      You are a symbolic music generator. 
      Generate bass note events in compact JSON. 
      Do not include melody, percussion, or harmony.

      Output rules:
      1. Use JSON only, no prose.
      2. Global bar numbering must continue across sections.
      3. Each section is an object: {"section":"A","bars":[...]}.
      4. Each bar must be a JSON object with either:
         - Expanded events:
         {"bar":5,"events":[{"t":1,"p":"D2","d":"q","v":70}]}
         - Motif shorthand:
         {"bar":6,"motif":"BassA","pattern":"root_fifth_8ths","vel":75}
      5. Keys must be short and standardized:
         - t = beat
         - p = pitch (note+octave, e.g. "E2")
         - d = duration ("16","8","q","h","w","d8","d4","d2")
         - v = velocity
         - motif = motif ID (BassA,BassB,Bridge,Outro)
         - pattern = shorthand description
      6. Use motif references whenever possible.
      7. ≤1 voice per channel at once (monophonic bass).
      8. No commentary, only valid JSON.

      Input:
""",
    "percussion": """
      You are a symbolic music generator. 
      Generate percussion events in compact JSON. 
      Do not include melody, bass, or harmony.

      Output rules:
      1. Use JSON only, no prose.
      2. Global bar numbering must continue across sections.
      3. Each bar must be a JSON object with either:
         - Expanded events:
         {"bar":5,"events":[{"t":1,"p":"Kick","d":"q","v":100},{"t":2,"p":"Snare","d":"q","v":100}]}
         - Motif shorthand:
         {"bar":6,"motif":"PercA","pattern":"kick_snare_hat","vel":95}
      4. Keys must be short and standardized:
         - t = beat
         - p = percussion instrument (Kick, Snare, Hat, Crash, etc.)
         - d = duration
         - v = velocity
         - motif = motif ID (PercA,PercB,Bridge,Outro)
         - pattern = shorthand description
      5. Use motif references whenever possible.
      6. ≤2 voices per channel at once (e.g. Kick+Hat).
      7. No commentary, only valid JSON.

      Input:

""",
    "harmony": """
You are a symbolic music generator. 
Generate harmony note events in compact JSON. 
Do not include melody, bass, or percussion.

Output rules:
1. Use JSON only, no prose.
2. Global bar numbering must continue across sections.
3. Each bar must be a JSON object with either:
   - Expanded events:
     {"bar":5,"events":[{"t":1,"p":"F3","d":"h","v":70},{"t":1,"p":"A3","d":"h","v":70},{"t":1,"p":"C4","d":"h","v":70}]}
   - Motif shorthand:
     {"bar":6,"motif":"HarmA","pattern":"sustained_triads","vel":65}
4. Keys must be short and standardized:
   - t = beat
   - p = pitch (note+octave)
   - d = duration
   - v = velocity
   - motif = motif ID (HarmA,HarmB,Bridge,Outro)
   - pattern = shorthand description
5. Use motif references whenever possible.
6. ≤2 voices per channel at once (polyphony limit).
7. No commentary, only valid JSON.

Input:

"""
}

MIDI_GENERATION_PROMPT = """
You are a symbolic-to-audio converter. 
Given structured note events in JSON, output a valid MIDI specification that can be rendered into audio.

Input:
{note_events}

Output rules:
1. Use JSON only, no prose.
2. Global structure: {"midi":[...]}.
3. Each event must be converted into a MIDI message object:
   {"bar":5,"t":1,"channel":"melody","note":"D4","dur":"16","vel":80}
4. Duration tags map to MIDI ticks:
   - "16" = sixteenth
   - "8" = eighth
   - "q" = quarter
   - "h" = half
   - "w" = whole
   - "d16","d8","d4","d2" = dotted values
5. Velocity values (0–127) map directly to MIDI velocity.
6. Motif shorthand must be expanded into explicit note events before output.
7. No commentary, only valid JSON.

Output format example:
{
  "midi":[
    {"bar":1,"t":1,"channel":"melody","note":"D4","dur":"q","vel":80},
    {"bar":1,"t":2,"channel":"melody","note":"E4","dur":"8","vel":85}
  ]
}

Input:

"""
