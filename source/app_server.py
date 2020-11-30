import logging

from images_api import CONFIG, app, routes
from images_api.scheduler import download_images

if __name__ == "__main__":
    download_images.delay()
    app.run("127.0.0.1", port=9999, debug=True)
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
