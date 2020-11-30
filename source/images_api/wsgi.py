from images_api import CONFIG
from images_api.scheduler import download_images


def on_starting(server):
    download_images.delay()


bind = "0.0.0.0:8080"

workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30

loglevel = CONFIG.get("api.log_lvl")
