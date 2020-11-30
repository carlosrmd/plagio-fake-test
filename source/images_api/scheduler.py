from . import CELERY, CONFIG, app
from .rest_api import ImageAPI
from .models import Image, ImageMetadata


def update_image(image):
    Image.objects(image_id=image["id"]).update_one(
        image_id=image.pop("id"),
        cropped_picture=image.pop("cropped_picture"),
        full_picture=image.pop("full_picture"),
        metadata=ImageMetadata(**image),
        upsert=True,
    )


@CELERY.task()
def download_images():
    image_object = ImageAPI(CONFIG.get("api.interview_api_key"))
    app.logger.info("Downloading image information")
    images = image_object.get_images_with_metadata()
    Image.objects(image_id__not__in=[image["id"] for image in images]).delete()
    list(map(update_image, images))
