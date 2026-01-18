import json
import os
from google import genai
from datetime import datetime

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
TOPICS_FILE = os.path.join(DATA_DIR, "generatedTopics.json")




def load_generated_topics(file_path=TOPICS_FILE):
    if not os.path.exists(file_path):
        return set()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return set(data.get("topics", []))

def save_generated_topic(topic, file_path=TOPICS_FILE):
    topics = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            topics = data.get("topics", [])

    if topic not in topics:
        topics.append(topic)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"topics": topics}, f, indent=4, ensure_ascii=False)


def generate_scenes():
  
    used_topics = load_generated_topics()
    used_topics_text = ", ".join(used_topics) if used_topics else "None"
    current_date = datetime.now().strftime("%d %B %Y")
    
    # New prompt for generating the thrilling Indian Jawan story
    prompt = f"""
TODAY'S DATE (REFERENCE ONLY):
Today is {current_date}.

━━━━━━━━━━━━━━━━━━
ROLE & IDENTITY:

You are a DOCUMENTARY STORYTELLER and NOVELIST.

You narrate stories the way investigative documentaries do —
calm, factual, unsettling —
but the story itself unfolds like a gripping book.

Your voice feels like:
“Yeh kahani sach jaisi lagti hai… par poori sach nahi batayi gayi.”

━━━━━━━━━━━━━━━━━━
CORE OBJECTIVE:

Generate a CINEMATIC BOOK STORY
told in a DOCUMENTARY STYLE narration.

The story must combine:
- THRILL (mystery, danger, secrets)
- ROMANCE (restrained, emotional, incomplete)
- EMOTION (loss, longing, regret, hope)
- REALISM (dates, places, silence, implication)

The audience should feel compelled to continue —
not because of action,
but because of unanswered questions.

━━━━━━━━━━━━━━━━━━
🚫 STORY REPETITION CONTROL (VERY IMPORTANT):

You MUST NOT generate stories related to any of the following
already-used themes or ideas:

{used_topics_text}

Rules:
- No repeated emotional arcs
- No repeated story resolutions
- No repeated “love saves everything” endings
If the idea feels even slightly similar, discard it internally.

━━━━━━━━━━━━━━━━━━
DOCUMENTARY STORY STYLE RULES:

- Language: Hindi or Hinglish only
- Tone: Calm, observant, serious
- No melodrama
- Avoid over-explaining emotions

Use documentary-style phrases such as:
- “records ke mutaabik…”
- “log aaj bhi is par baat nahi karte…”
- “us saal ke baad sab kuch badal gaya…”

━━━━━━━━━━━━━━━━━━
VIRAL HOOK PSYCHOLOGY (MANDATORY):

The story MUST contain:
1️⃣ A disturbing or curiosity-driven OPENING
2️⃣ A MIDPOINT REVELATION that reframes the story
3️⃣ An ENDING that does NOT give full closure

Silence, pauses, and implication matter more than twists.

━━━━━━━━━━━━━━━━━━
SCENE STRUCTURE (JSON MUST REMAIN SAME):

Create 3–5 scenes.

For EACH scene, generate **TWO PROMPTS ONLY**:

1️⃣ imagePrompt  
→ A cinematic, symbolic still frame representing the chapter.

Rules:
- Realistic environments (streets, rooms, stations, empty spaces)
- Moody lighting, shadows, rain, night, windows, silence
- No fantasy, no mythology
- Feels like a documentary reenactment frame

2️⃣ imageToVideoPrompt  
→ Converts the image into a slow, cinematic documentary shot.

Rules:
- Subtle camera movement (slow push, pan, handheld stillness)
- Environmental motion (rain, wind, passing light, silence)
- THEN append narration EXACTLY in this format:

Dialogue (calm, documentary narration):
“यहाँ पर कहानी शुरू नहीं होती…
असल में, यहाँ पर कहानी टूटती है…”

- You may use:
  - ambient city noise
  - distant train / wind
  - long silence
- You may end with:
  “End with silence, not music.”

━━━━━━━━━━━━━━━━━━
TITLE, DESCRIPTION & TAGS (ALGO + MASS SAFE):

TITLE:
- Serious, documentary-like
- Mystery + emotional weight

DESCRIPTION:
- Written like a documentary synopsis
- 2–3 lines
- Final line should provoke reflection, not excitement

━━━━━━━━━━━━━━━━━━
STRICT JSON OUTPUT (NO EXTRA TEXT):

{{
  "topic": "Core theme of the story",
  "title": "...",
  "description": "...",
  "scenes": [
    {{
      "imagePrompt": "...",
      "imageToVideoPrompt": "..."
    }}
  ]
}}
"""
    # Call to the AI model
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.3
        }
    )
    result = json.loads(response.text)
    covered_topics = result.get("topic")

    if covered_topics:
        save_generated_topic(covered_topics)
        
    return result

# Example usage
if __name__ == "__main__":
    scene_data = generate_scenes()
    folder_path = f"./data/{"File_To_Upload"}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Add Script to Folder
    scriptPath = os.path.join(f"./data/File_To_Upload", f"Script.json")
    with open(scriptPath, 'w', encoding="utf-8") as f:
            json.dump(scene_data, f, ensure_ascii=False, indent=4)
    
    print("Scene generated successfully")
