import os
import json
from src.script_writer import generate_scenes
from src.generateImage import generate_image
from src.generateVideo import generate_video
from src.generateClips import generate_image_to_video
from src.imageUploader import upload_image_to_cloudinary

def run():
    scene_data = generate_scenes()
    
    # Create a folder for the video ID if it doesn't exist
    folder_path = f"./data/{"File_To_Upload"}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Add Script to Folder
    scriptPath = os.path.join(f"./data/File_To_Upload", f"Script.json")
    with open(scriptPath, 'w', encoding="utf-8") as f:
            json.dump(scene_data, f, ensure_ascii=False, indent=4)
    
    print("Scene generated successfully")
    
    # Generate images and audio for each scene
    for i in range(len(scene_data['scenes'])):
        prompt = scene_data['scenes'][i]['imagePrompt']
        videoPrompt  = scene_data['scenes'][i]['imageToVideoPrompt']
        imagepath = generate_image(prompt , i, "File_To_Upload")  
        imageUrl = upload_image_to_cloudinary(imagepath)
        generate_image_to_video(videoPrompt,imageUrl,i,"File_To_Upload" )
    
    # Create the final video from the images and audio
    generate_video("File_To_Upload", scene_data, folder_path)

if __name__ == "__main__":
    run()
