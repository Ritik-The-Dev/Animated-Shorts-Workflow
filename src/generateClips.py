import http.client
import urllib.parse
import os


def generate_image_to_video(
    prompt: str,
    image_url: str,
    scene_number: int,
    folder_name: str
):
    # ---------- API KEY ----------
    headers = {
    'Authorization': 'Bearer sk_Jp9S2kIw9bFfq5ANd7LKIvGi1FzcLCYu'
    }

    # ---------- QUERY PARAMETERS ----------
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

    # ---------- API REQUEST ----------
    conn = http.client.HTTPSConnection("gen.pollinations.ai")
    conn.request("GET", endpoint, headers=headers)

    response = conn.getresponse()
    data = response.read()
    content_type = response.getheader("Content-Type", "")

    conn.close()

    # ---------- VALIDATION ----------
    if response.status != 200:
        raise RuntimeError(
            f"API Error {response.status}: {data[:300]}"
        )

    if "video" not in content_type:
        raise ValueError(
            f"Expected video but received '{content_type}'. "
            f"Response preview: {data[:200]}"
        )

    # ---------- SAVE OUTPUT ----------
    folder_path = os.path.join("data", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    video_path = os.path.join(folder_path, f"Scene{scene_number}.mp4")

    with open(video_path, "wb") as f:
        f.write(data)

    print(f"✅ Scene {scene_number} saved → {video_path}")
