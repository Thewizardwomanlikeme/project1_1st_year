from dotenv import load_dotenv
from imagekitio import ImageKit
from pathlib import Path
import os

'''ImageKit stores the image.
SQLite (test.db) stores information about the image.

note:
async def  → await it

def        → don't await it'''

dotenv_path = Path(__file__).resolve().parents[1] / ".env"  # Find the .env file located two folders above this Python file and save its path in dotenv_path.
'''__file__ is the path of the Python file currently being executed like in this case project/backend/img_vid.py
Path converts the path (project/backend/img_vid.py) into an object which makes it easier to work with file/folder paths.
.resolve converts it into a absolute (complete) path like C: /Users/Anjali/project/backend/images.py - it should actually backslash
/ here acts like a appender

The parents are:
parents[0] → C:/Users/Anjali/project/backend
parents[1] → C:/Users/Anjali/project
parents[2] → C:/Users/Anjali

Path(__file__).resolve().parents[1] means: Go up two directory levels from the current Python file - C: /Users/Anjali/project/backend/images.py
'''

load_dotenv(dotenv_path=dotenv_path) # this line loads all the .env secrets into the current file so that line 29 can run.

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

    extension = Path(file_name).suffix.lower()
    if extension == ".gif":
        file_type = "gif"
    elif extension in {".mp4", ".webm"}:
        file_type = "video"
    elif extension in {".jpg", ".jpeg", ".png"}:
        file_type = "image"
    else:
        file_type = result.file_type

    return {
        "url": result.url,
        "file_name": result.name,
        "file_type": file_type,
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