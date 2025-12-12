import os
import json
from openai import OpenAI
from prompts import *
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenRouter client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def prompt_llm(user_message: str, system_message: str = None, model: str = "mistralai/devstral-2512:free", 
               temperature: float = 0.8, max_tokens: int = 2500) -> list:
    """
    Prompts the LLM with any message and returns the response.
    Args:
        user_message (str): The message to send to the LLM.
    Returns:
        list: Parsed JSON response from the LLM.
    """
    if not system_message:
        system_message = "You are a helpful assistant."
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response_text = response.choices[0].message.content
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON response: {response_text}")
        return []


def define_music_plan(theme: str) -> str:
    system_prompt = DEFINE_MUSIC_PLAN_PROMPT
    user_prompt = f"Create a detailed music composition plan for the following theme: '{theme}'."
    return prompt_llm(user_prompt, system_prompt)

def define_music_chord_rtythm(theme: str, music_plan: str) -> str:
    system_prompt = DEFINE_CHORD_RHYTHM_PROMPT.format(music_plan=music_plan)
    user_prompt = f"Create detailed chord progressions and rhythm grids for the following music outline based on the theme: '{theme}'."
    return prompt_llm(user_prompt, system_prompt)

if __name__ == "__main__":
    theme = "retro 8-bit battle theme"
    plan = define_music_plan(theme)
    chord_rhythm = define_music_chord_rtythm(theme, plan)
    for item in chord_rhythm:
        print(item)
