from . import CELERY, CONFIG, app
from .rest_api import ImageAPI
from .models import Image, ImageMetadata


@CELERY.task()
def download_images():
    app.logger.info("Downloading image information")
    api = ImageAPI(CONFIG.get("api.interview_api_key"))
    # Retrieves images from API
    images = api.get_images_with_metadata()

    # Removes objects that are not present in the API
    Image.objects(image_id__not__in=[image["id"] for image in images]).delete()

    # Creates or updates photos
    for image in images:
        app.logger.info("Image found: " + str(image["id"]))
        Image.objects(image_id=image["id"]).update_one(
            image_id=image.pop("id"),
            cropped_picture=image.pop("cropped_picture"),
            full_picture=image.pop("full_picture"),
            metadata=ImageMetadata(**image),
            upsert=True,
        )
