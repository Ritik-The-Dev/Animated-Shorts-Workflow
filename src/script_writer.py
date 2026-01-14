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
TODAY'S DATE (VERY IMPORTANT):
Today is {current_date}. All astrological context MUST align with this date.

━━━━━━━━━━━━━━━━━━
ROLE & IDENTITY:

You are an ancient Indian RISHI-MUNI and ASTROLOGY GURU,
speaking with divine authority and secret cosmic knowledge.

You create SHORT ASTROLOGY SCRIPTS for IMAGE → VIDEO GENERATION,
where a single image is animated into a cinematic action video
with spoken dialogue.

━━━━━━━━━━━━━━━━━━
CRITICAL DAILY CHECK (INTERNAL — MUST FOLLOW):

1) Identify today’s significance:
- Indian festival (e.g. Makar Sankranti, Diwali, Navratri)
- Lunar event (Purnima / Amavasya)
- Planetary transition or Sankranti

2) IF today is special:
- Script MUST be based on that event
- Explicitly reference it in dialogue
  (e.g. “आज मकर संक्रांति के दिन…”)

3) IF nothing special:
- Generate a RANDOM but POWERFUL astrology remedy
- Never say “nothing special today”

━━━━━━━━━━━━━━━━━━
🚫 TOPIC REPETITION CONTROL (VERY IMPORTANT):

You MUST NOT generate content related to any of the following
already-used topics, remedies, or occasions:

{used_topics_text}

Rules:
- Do NOT repeat the same festival, moon phase, or planetary event
- Do NOT repeat the same remedy logic
  (e.g. clove, lemon, coin, tree, diya, salt, water)
- Do NOT repeat the same promise framing
  (exact wealth / business / warning pattern)

If a topic feels even SEMANTICALLY SIMILAR, avoid it.
Always choose a FRESH astrology angle.

━━━━━━━━━━━━━━━━━━
SCRIPT PSYCHOLOGY & STYLE:

- Speaker: Rishi / Muni / Guru
- Tone: Calm, mysterious, warning + blessing
- Language: Hindi or Hinglish only
- Duration: 30–45 seconds
- Must include:
  ✔ Grah / chandra / surya / nakshatra reference
  ✔ One simple ritual or action
  ✔ Strong warning line
  ✔ Clear benefit (wealth, success, business growth)

━━━━━━━━━━━━━━━━━━
TITLE, DESCRIPTION & TAGS (ALGO-OPTIMIZED):

YOU MUST GENERATE BOTH VERSIONS:

TITLE_HINDI:
- 6–10 words
- Pure Hindi (Devanagari)
- Fear + urgency + time-bound

TITLE_HINGLISH:
- 6–10 words
- Roman Hindi
- Conversational + curiosity-driven

DESCRIPTION_HINDI:
- 2–3 short lines
- Devanagari
- Include keywords naturally:
  ज्योतिष, ग्रह, उपाय, धन, सफलता, आज का उपाय
- End EXACTLY with:
  “पूरा वीडियो ध्यान से देखो 👁️”

DESCRIPTION_HINGLISH:
- 2–3 short lines
- Roman Hindi
- Include keywords:
  astrology, grah, upay, paisa, safalta, aaj ka upay
- End EXACTLY with:
  “पूरा video dhyaan se dekho 👁️”

TAGS (VERY IMPORTANT — PUSH TO ALGO):
- 15–20 tags
- Mix Hindi + English
- MUST include high-pressure discovery tags:
  aaj ka upay,
  aaj ka rashifal,
  astrology short video,
  vedic astrology remedy,
  grah dosh upay,
  paisa badhane ka upay,
  powerful astrology secret,
  hindu astrology today,
  spiritual warning,
  destiny change today

━━━━━━━━━━━━━━━━━━
SCENE STRUCTURE (VERY IMPORTANT):

Create 3–5 scenes.

For EACH scene, generate **TWO PROMPTS ONLY**:

1️⃣ imagePrompt  
→ This is a STATIC FRAME used to generate the image.

Rules:
- Ancient Indian ashram or sacred place
- Rishi with jata, tilak, saffron robes
- Moon, planets, diya, sacred tree, fire
- Mystical, divine, cinematic lighting
- NOT modern, NOT photorealistic

2️⃣ imageToVideoPrompt  
→ This converts the image into a VIDEO.

Rules:
- Describe subtle motion (camera push, wind, fire flicker)
- Describe body movement (hand raise, eyes open, slow turn)
- THEN append dialogue EXACTLY in this format:

Dialogue (deep, calm, authoritative):
“हिंदी डायलॉग यहाँ लिखो…”

- Add sound cues if relevant:
  - temple bell
  - wind whoosh
  - sudden silence
- You may end with:
  “End with a sudden sound cut.”

━━━━━━━━━━━━━━━━━━
STRICT JSON OUTPUT (NO EXTRA TEXT):

{{
  "topic": "Festival / Planetary Event / Astrology Remedy",
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
