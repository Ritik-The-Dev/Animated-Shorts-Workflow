import http.client
import urllib.parse
import os
import time
import random


def generate_image_to_video(
    prompt: str,
    image_url: str,
    scene_number: int,
    folder_name: str,
    max_retries: int = 3,
    cooldown_seconds: float = 2.5
):
    headers = {
        'Authorization': 'Bearer sk_Jp9S2kIw9bFfq5ANd7LKIvGi1FzcLCYu'
    }

    query_params = {
        "model": "veo",
        "width": 1080,
        "height": 1920,
        "seed": 0,
        "enhance": "false",
        "negative_prompt": "worst quality, blurry",
        "safe": "false",
        "quality": "hd",
        "image": image_url,
        "transparent": "false",
        "duration": 8,
        "audio": "true"
    }

    encoded_prompt = urllib.parse.quote(prompt)
    encoded_query = urllib.parse.urlencode(query_params)
    endpoint = f"/image/{encoded_prompt}?{encoded_query}"

    folder_path = os.path.join("data", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    video_path = os.path.join(folder_path, f"Scene{scene_number}.mp4")

    # ---------- RETRY LOOP ----------
    for attempt in range(1, max_retries + 1):
        try:
            conn = http.client.HTTPSConnection("gen.pollinations.ai", timeout=120)
            conn.request("GET", endpoint, headers=headers)

            response = conn.getresponse()
            data = response.read()
            content_type = response.getheader("Content-Type", "")

            conn.close()

            # ---------- SUCCESS ----------
            if response.status == 200 and "video" in content_type:
                with open(video_path, "wb") as f:
                    f.write(data)

                print(f"✅ Scene {scene_number} saved → {video_path}")
                time.sleep(cooldown_seconds)
                return

            # ---------- SERVER ERROR (RETRYABLE) ----------
            if response.status >= 500:
                wait = (2 ** attempt) + random.uniform(0.5, 1.5)
                print(
                    f"⚠️ Scene {scene_number} attempt {attempt}/{max_retries} "
                    f"failed with {response.status}. Retrying in {wait:.1f}s"
                )
                time.sleep(wait)
                continue

            # ---------- CLIENT / CONTENT ERROR (FAIL FAST) ----------
            raise RuntimeError(
                f"API Error {response.status}: {data[:300]}"
            )

        except Exception as e:
            if attempt == max_retries:
                raise RuntimeError(
                    f"❌ Scene {scene_number} failed after {max_retries} retries.\n{e}"
                )
            wait = (2 ** attempt) + random.uniform(0.5, 1.5)
            print(
                f"⚠️ Scene {scene_number} exception on attempt {attempt}/{max_retries}: {e}\n"
                f"Retrying in {wait:.1f}s"
            )
            time.sleep(wait)

