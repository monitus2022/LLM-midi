import json

from prompts import *
from utils import timeit
from llm import OpenrouterLlm, OllamaLlm
import os
import concurrent.futures

midi_llm = OpenrouterLlm()
# prompt_llm = OllamaLlm().prompt_llm


@timeit
def define_music_plan(theme: str) -> str:
    system_prompt = DEFINE_MUSIC_PLAN_PROMPT
    user_prompt = f"Create a detailed music composition plan for the following theme: '{theme}'."
    return midi_llm.prompt_llm(user_prompt, system_prompt)


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

# @timeit
# def note_events_from_plan(chord_rhythm_plan: str) -> str:
#     system_prompt = NOTE_EVENTS_PROMPT + str(chord_rhythm_plan)
#     user_prompt = f"Generate structured note events based on the following chord and rhythm plan."
#     response = midi_llm.prompt_llm(user_prompt, system_prompt)
#     return midi_llm.json_response(response)


@timeit
def note_events_for_channel(channel: str, note_events_prompt: str, chrod_rhythm_plan: str) -> str:
    system_prompt = note_events_prompt.replace(
        "__CHANNEL__", channel) + str(chrod_rhythm_plan)
    user_prompt = f"Generate structured note events for the {channel} channel based on the provided plan."
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

    with open("../output/chord_rhythm_plan.json", "r") as f:
        chord_rhythm_plan = json.load(f)

    channel_prompt = NOTE_EVENTS_PROMPT
    all_events = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(
                note_events_for_channel, channel, channel_prompt, chord_rhythm_plan
            ) : channel
            for channel in ALL_CHANNELS
        }
        for future in concurrent.futures.as_completed(futures):
            channel = futures[future]
            try:
                result = future.result()
                all_events[channel] = result
            except Exception as e:
                print(f"Error generating events for a channel: {e}")

    with open("../output/note_events.json", "w") as f:
        json.dump(all_events, f, indent=4)

    print("Music composition generation complete.")
