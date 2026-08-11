from dotenv import load_dotenv
from imagekitio import ImageKit
from pathlib import Path
import os

'''ImageKit stores the image.
SQLite (test.db) stores information about the image.

note:
async def  → await it

def        → don't await it'''

dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)

private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")

imagekit = None
if private_key:
    imagekit = ImageKit(
        private_key=private_key,
    )

MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB, 1MB = 1024*1024 bytes
ALLOWED_MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm")


def upload_to_imagekit(file_bytes: bytes, file_name: str, folder: str = "posts"): # if folder is not specified then default to posts
    if imagekit is None:
        raise RuntimeError("ImageKit is not configured. Set IMAGEKIT_PRIVATE_KEY first.")

    normalized_name = file_name.lower() # .lower beacuse .JPG and .jpg are different to python but then we want python to accept both
    if not normalized_name.endswith(ALLOWED_MEDIA_EXTENSIONS): # endswith() asks: "Does this string end with one of these things?" | "cat.jpg".endswith(".jpg") gives: True
        raise ValueError(
            "Unsupported file type. Only JPG, JPEG, PNG, GIF, MP4, and WEBM files are allowed."
        )

    if len(file_bytes) > MAX_UPLOAD_SIZE_BYTES: 
        raise ValueError(
            f"Upload exceeded the maximum allowed size of {MAX_UPLOAD_SIZE_BYTES // 1024 // 1024} MB." #52,428,800 // 1024 converts bytes → KB. Then: // 1024 converts KB → MB.
        )

    result = imagekit.files.upload(
        file=file_bytes,
        file_name=file_name,
        folder=folder,
        use_unique_file_name=True,
    )

    return {
        "url": result.url,
        "file_name": result.name,
        "file_type": result.file_type,
    }

'''         USER UPLOADS FILE
                 ↓
     Is ImageKit configured?
            ↙          ↘
          NO            YES
          ↓              ↓
        ERROR       Convert filename
                        to lowercase
                           ↓
            Is extension allowed?
                 ↙          ↘
               NO           YES
               ↓             ↓
             ERROR       Check file size
                              ↓
                     Is it ≤ 50 MB?
                       ↙          ↘
                     NO           YES
                     ↓             ↓
                   ERROR       Continue with
                              ImageKit upload'''