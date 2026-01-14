from PIL import Image

# Fix for Pillow >= 10
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import VideoFileClip, CompositeVideoClip
import os

# Target portrait resolution
PORTRAIT_WIDTH = 1080
PORTRAIT_HEIGHT = 1920

# Optional landscape resolution (keep original or set max width/height)
LANDSCAPE_WIDTH = 1920
LANDSCAPE_HEIGHT = 1080

def generate_video(vid, scene_data, folder_path):
    portrait_clips = []
    landscape_clips = []
    timeline_portrait = 0
    timeline_landscape = 0

    for i, _ in enumerate(scene_data["scenes"]):
        scene_path = os.path.join(folder_path, f"Scene{i}.mp4")

        if not os.path.exists(scene_path):
            raise FileNotFoundError(f"Missing scene file: {scene_path}")

        clip = VideoFileClip(scene_path)
        w, h = clip.size

        ### --- PORTRAIT VERSION ---
        portrait_clip = clip

        # Crop to portrait aspect ratio
        if w/h > PORTRAIT_WIDTH/PORTRAIT_HEIGHT:
            # wider than portrait -> crop width
            new_w = int(h * PORTRAIT_WIDTH / PORTRAIT_HEIGHT)
            x1 = (w - new_w) // 2
            portrait_clip = portrait_clip.crop(x1=x1, y1=0, x2=x1+new_w, y2=h)
        elif w/h < PORTRAIT_WIDTH/PORTRAIT_HEIGHT:
            # taller than portrait -> crop height
            new_h = int(w * PORTRAIT_HEIGHT / PORTRAIT_WIDTH)
            y1 = (h - new_h) // 2
            portrait_clip = portrait_clip.crop(x1=0, y1=y1, x2=w, y2=y1+new_h)

        portrait_clip = portrait_clip.resize((PORTRAIT_WIDTH, PORTRAIT_HEIGHT))

        # Crossfade / timing
        if not portrait_clips:
            portrait_clip = portrait_clip.set_start(timeline_portrait)
        else:
            portrait_clip = portrait_clip.set_start(timeline_portrait - 0.6).crossfadein(0.6)
        timeline_portrait += portrait_clip.duration
        portrait_clips.append(portrait_clip)

        ### --- LANDSCAPE VERSION ---
        landscape_clip = clip

        # Optional: Resize to max landscape resolution while keeping aspect ratio
        landscape_clip = landscape_clip.resize(height=LANDSCAPE_HEIGHT)
        # If width exceeds max, resize by width
        if landscape_clip.w > LANDSCAPE_WIDTH:
            landscape_clip = landscape_clip.resize(width=LANDSCAPE_WIDTH)

        # Crossfade / timing
        if not landscape_clips:
            landscape_clip = landscape_clip.set_start(timeline_landscape)
        else:
            landscape_clip = landscape_clip.set_start(timeline_landscape - 0.6).crossfadein(0.6)
        timeline_landscape += landscape_clip.duration
        landscape_clips.append(landscape_clip)

    if not portrait_clips or not landscape_clips:
        raise RuntimeError("No valid scenes were generated. Video aborted.")

    # Export portrait
    final_portrait = CompositeVideoClip(portrait_clips)
    portrait_path = os.path.join(folder_path, f"{vid}_final_video.mp4")
    final_portrait.write_videofile(
        portrait_path,
        fps=24,
        audio_codec="aac",
        threads=4
    )

    # Export landscape
    final_landscape = CompositeVideoClip(landscape_clips)
    landscape_path = os.path.join(folder_path, f"{vid}_final_video_landscape.mp4")
    final_landscape.write_videofile(
        landscape_path,
        fps=24,
        audio_codec="aac",
        threads=4
    )

    print(f"\n✅ Portrait video saved: {portrait_path}")
    print(f"✅ Landscape video saved: {landscape_path}\n")
