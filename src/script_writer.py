import json
import os
import uuid
from google import genai
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "File_To_Upload")

STORY_STATE_FILE = os.path.join(DATA_DIR, "storyState.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# STORY MEMORY (ONLY SOURCE OF TRUTH)
# ─────────────────────────────────────────────

def load_previous_story(file_path=STORY_STATE_FILE):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_story_state(story_data, file_path=STORY_STATE_FILE):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(story_data, f, indent=4, ensure_ascii=False)

# ─────────────────────────────────────────────
# CORE GENERATION
# ─────────────────────────────────────────────

def generate_scenes():
    # previous_story = load_previous_story()
    
    prompt = f"""
Create a cinematic animated short scene sequence.

STYLE:
Hand-drawn animated look.
Soft anime-style illustration.
Non-realistic proportions.
Painterly backgrounds, gentle lighting.
Fantasy science-fiction tone.
No realism. No live-action look.

LANGUAGE:
Narration and dialogue in Hindi (Devanagari only).

CHARACTER DESIGN (IMPORTANT):
- Animated character
- Simplified facial features
- No realistic skin texture
- Expressive but stylized
- Childlike proportions without realism

SCENE CONCEPT:
An animated young genius with secret technology lives a double life.
To the world, he appears to be a normal school-going child.
His abilities and devices remain unseen by others.

OPENING SCENE:
A dreamy sky filled with soft clouds at dawn.
A small animated figure descends gently through the air.
A softly glowing energy core shines through a stylized chest device.

Calm narration (Hindi, Devanagari):
“आज भी यह पूरी तरह तैयार नहीं है…”

The character speaks softly to an unseen system:
“सिस्टम… सक्रिय हो?
मुझे स्कूल के लिए देर नहीं होनी चाहिए।”

VISUAL ELEMENTS TO INCLUDE ACROSS SCENES:
- Animated mechanical arms assembling clothes in mid-air
- Stylized boots enabling gentle flight
- Smooth animated transition from sky → town → school area
- Background characters remain unaware and unfocused

STORY FLOW:
- Scene 1: Gentle descent through clouds
- Scene 2: Automated preparation in the air
- Scene 3: Quiet animated flight above rooftops
- Scene 4: Landing near school, technology fades away
- Scene 5: Character blends in as a normal student

ENDING TWIST:
A small animated warning symbol flickers briefly on the chest device,
visible only to the audience.

OUTPUT REQUIREMENTS:
Return STRICT JSON only.

FORMAT:
{{
  "script": "continuous narration and dialogue in Hindi (Devanagari)",
  "scenes": [
    {{
      "sceneNumber": 1,
      "imagePrompt": "animated visual description only",
      "imageToVideoPrompt": "camera motion, ambient sound, and spoken lines"
    }}
  ]
}}
"""
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.3
        }
    )

    result = json.loads(response.text)

    # save_story_state({ "currentStory" : previous_story.get("currentStory") + result["script"]})
    return result

# ─────────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────────

if __name__ == "__main__":
    story_data = generate_scenes()

    script_path = os.path.join(UPLOAD_DIR, "Script.json")
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(story_data, f, ensure_ascii=False, indent=4)

    print("✅ Story continued and saved successfully.")
