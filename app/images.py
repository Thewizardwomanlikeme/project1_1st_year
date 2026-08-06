from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

private_key = os.getenv("IMAGEKIT_PRIVATE_KEY") 
url_endpoint = os.getenv("IMAGEKIT_URL")

imagekit = None
if private_key and url_endpoint:
    imagekit = ImageKit(
        private_key=private_key,
        url_endpoint=url_endpoint,
    )


def upload_to_imagekit(file_bytes: bytes, file_name: str, folder: str = "posts"):
    if imagekit is None:
        raise RuntimeError("ImageKit is not configured. Set IMAGEKIT_PRIVATE_KEY and IMAGEKIT_URL first.")

    result = imagekit.files.upload(
        file=file_bytes,
        file_name=file_name,
        folder=folder,
        use_unique_file_name=True,
    )

    return result.url if hasattr(result, "url") else None