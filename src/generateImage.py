import http.client
import urllib.parse
import os
from PIL import Image

conn = http.client.HTTPSConnection("gen.pollinations.ai")
# ChannelFace = "https://res.cloudinary.com/dw4gtg42m/image/upload/v1768364007/Whisk_d444022aa64aeb59775410354c7217ebdr_mvocjr.png"
headers = {
    'Authorization': 'Bearer sk_Jp9S2kIw9bFfq5ANd7LKIvGi1FzcLCYu'
}

def generate_image(prompt , sceneNumber, folderName, max_retries=3):
    # URL encode the prompt for the API request
    encoded_request = urllib.parse.quote(prompt)
    modelNames = ['gptimage' ,'seedream-pro' ,'kontext']
    # Generate the image and save it
    for attempt in range(max_retries):
        # Make the API request
        # conn.request("GET", f"/image/{encoded_request}?model={modelNames[attempt]}&width=1080&height=1920&image={ChannelFace}", headers=headers)
        conn.request("GET", f"/image/{encoded_request}?model={modelNames[attempt]}&width=1080&height=1920", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        # Ensure the directory exists
        folder_path = f"./data/{folderName}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder if it doesn't exist
        
        # Save the image in the specified folder
        image_path = os.path.join(folder_path, f"Image{sceneNumber}.png")
        with open(image_path, 'wb') as f:
            f.write(data)

        print(f"Image saved as '{image_path}'")

        # Check if the image can be loaded correctly
        try:
            with Image.open(image_path) as img:
                img.verify()  # Verify if image is valid
            print(f"Image '{image_path}' loaded successfully.")
            return image_path  
        except (IOError, SyntaxError) as e:
            print(f"Error loading image with model {modelNames[attempt]} : {e}")
            print(f"Retrying image generation with model {modelNames[attempt + 1]} ... (Attempt {attempt + 1} of {max_retries})")
            # If image is not valid, retry generating the image
            if attempt == max_retries - 1:
                print(f"Failed to generate a valid image after {max_retries} attempts.")
                return None  # Return None if all attempts fail