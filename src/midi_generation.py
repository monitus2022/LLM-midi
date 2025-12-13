import json

from prompts import *
from utils import timeit
from llm import OpenrouterLlm, OllamaLlm
import os

midi_llm = OpenrouterLlm()
# prompt_llm = OllamaLlm().prompt_llm

@timeit
def define_music_plan(theme: str) -> str:
    system_prompt = DEFINE_MUSIC_PLAN_PROMPT
    user_prompt = f"Create a detailed music composition plan for the following theme: '{theme}'."
    return midi_llm.prompt_llm(user_prompt, system_prompt)

# @timeit
# def define_music_chord_rtythm(theme: str, music_plan: str) -> str:
#     system_prompt = DEFINE_CHORD_RHYTHM_PROMPT.format(music_plan=music_plan)
#     user_prompt = f"Create detailed chord progressions and rhythm grids for the following music outline based on the theme: '{theme}'."
#     return prompt_llm(user_prompt, system_prompt)

@timeit
def define_music_chord(theme: str, music_plan: str) -> str:
    system_prompt = DEFINE_CHORD_PROMPT + music_plan
    user_prompt = f"Create detailed chord progressions for the following music outline based on the theme: '{theme}'."
    response = midi_llm.prompt_llm(user_prompt, system_prompt)
    return midi_llm.json_response(response)

@timeit
def define_rtythm_grid(theme: str, chord_backbone: str) -> str:
    system_prompt = DEFINE_RHYTHM_PROMPT + str(chord_backbone)
    user_prompt = f"Create detailed rhythm grids for the following music outline based on the theme: '{theme}'."
    response = midi_llm.prompt_llm(user_prompt, system_prompt)
    return midi_llm.json_response(response)

@timeit
def note_events_from_plan(chord_rhythm_plan: str) -> str:
    system_prompt = NOTE_EVENTS_PROMPT + str(chord_rhythm_plan)
    user_prompt = f"Generate structured note events based on the following chord and rhythm plan."
    response = midi_llm.prompt_llm(user_prompt, system_prompt)
    return midi_llm.json_response(response)

@timeit
def generate_midi(note_events: str) -> str:
    system_prompt = MIDI_GENERATION_PROMPT + str(note_events)
    user_prompt = f"Convert the following note events to MIDI specification: {note_events}"
    response = midi_llm.prompt_llm(user_prompt, system_prompt)
    return midi_llm.json_response(response)

if __name__ == "__main__":
    print("Generating music composition...")
    theme = "retro 8-bit battle theme"

    # plan = define_music_plan(theme)
    # with open("../output/music_plan.txt", "w") as f:
    #     f.write(plan)

    # chord_backbone = define_music_chord(theme, plan)
    # with open("../output/chord_backbone.json", "w") as f:
    #     json.dump(chord_backbone, f, indent=4)

    # chord_rhythm_plan = define_rtythm_grid(theme, chord_backbone)
    # with open("../output/chord_rhythm_plan.json", "w") as f:
    #     json.dump(chord_rhythm_plan, f, indent=4)

    # note_events = note_events_from_plan(chord_rhythm_plan)
    # with open("../output/note_events.json", "w") as f:
    #     json.dump(note_events, f, indent=4)
    with open("../output/note_events.json", "r") as f:
        note_events = json.load(f)
    midi_spec = generate_midi(note_events)
    with open("../output/midi_spec.json", "w") as f:
        json.dump(midi_spec, f, indent=4)

    print("Music composition generation complete.")
    
