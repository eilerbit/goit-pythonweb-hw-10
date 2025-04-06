import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage

class UploadFileService:
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

    def upload_file(self, file, username: str) -> str:
        public_id = f"RestApp/{username}"
        # Upload the file to Cloudinary; file.file is the underlying file object from UploadFile
        result = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
        # Build the URL with fixed dimensions (250x250)
        src_url = CloudinaryImage(public_id).build_url(width=250, height=250, crop="fill", version=result.get("version"))
        return src_url
