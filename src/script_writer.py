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
    previous_story = load_previous_story()
    current_date = datetime.now().strftime("%d %B %Y")

    # ── Continuation Context ──
    previous_context = ""
    story_id = str(uuid.uuid4())

    if previous_story:
        story_id = previous_story.get("storyId", story_id)
        previous_context = f"""
PREVIOUS STORY (MANDATORY CONTINUATION):

Title:
{previous_story.get("title")}

Current Story Summary:
{previous_story.get("previousSummary")}

Last Known Narration (for continuity):
{previous_story.get("script")[-800:]}

Rules:
- This is the SAME story
- Continue forward in time
- Do NOT reintroduce characters
- Do NOT re-explain past events
- Every scene must be a consequence of the previous one
"""

    prompt = f"""
TODAY'S DATE (REFERENCE ONLY):
{current_date}

━━━━━━━━━━━━━━━━━━
ROLE:

You are a DOCUMENTARY STORYTELLER.

Your narration is:
Calm. Observational. Investigative.
Emotion exists in pauses, not words.

━━━━━━━━━━━━━━━━━━
{previous_context}

━━━━━━━━━━━━━━━━━━
CORE OBJECTIVE:

Continue the SAME documentary-style story.

If no previous story exists:
- Begin a NEW story that feels real and unsettling

If a previous story exists:
- Continue it naturally, as if episodes are unfolding

━━━━━━━━━━━━━━━━━━
MANDATORY STRUCTURE:

- Generate AT LEAST 5 SCENES (never fewer)
- Each scene must directly depend on the previous one
- No scene resets
- Emotional and narrative progression must be linear

━━━━━━━━━━━━━━━━━━
DOCUMENTARY STYLE RULES:

- Language: Hindi / Hinglish only
- No melodrama
- Avoid explaining emotions
- Use implication, silence, factual phrasing

Use phrases like:
- “records ke mutaabik…”
- “is baat ka koi official jawab nahi mila…”
- “uske baad jo hua, woh likha nahi gaya…”

━━━━━━━━━━━━━━━━━━
FOR EACH SCENE (ONLY TWO PROMPTS):

1) imagePrompt
- Cinematic, realistic still frame
- Documentary reenactment feel
- Real locations, moody lighting

2) imageToVideoPrompt
- Slow camera motion
- Ambient sound, silence
- Must INCLUDE calm narration text

━━━━━━━━━━━━━━━━━━
ALSO GENERATE:

1) FULL CONTINUOUS DOCUMENTARY SCRIPT (all scenes combined)
2) ONE-PARAGRAPH SUMMARY of where the story now stands

━━━━━━━━━━━━━━━━━━
STRICT JSON OUTPUT ONLY:

{{
  "storyId": "{story_id}",
  "title": "...",
  "description": "...",
  "previousSummary": "...",
  "script": "Full documentary narration text",
  "scenes": [
    {{
      "sceneNumber": 1,
      "imagePrompt": "...",
      "imageToVideoPrompt": "..."
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

    save_story_state(result)
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
