import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dvgcxl8gc",
    api_key="625559286535851",
    api_secret="xNVeqhQfH8PFsGGgQS6C8ikfvn0",
    secure=True
)


def upload_image_to_cloudinary(image_path, folder="ai-video-images"):
    """
    Uploads image to Cloudinary and returns secure public URL
    """

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    result = cloudinary.uploader.upload(
        image_path,
        folder=folder,
        resource_type="image",
        overwrite=True
    )

    return result["secure_url"]
