from flask import Flask
from flask_caching import Cache
from flask_mongoengine import MongoEngine

import config_pkg
from celery import Celery

CONFIG = config_pkg.PKG()
CONFIG.load()

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
    "host": CONFIG.get("mongodb.host"),
    "port": CONFIG.get("mongodb.port"),
    "db": CONFIG.get("mongodb.db"),
    "username": CONFIG.get("mongodb.username"),
    "password": CONFIG.get("mongodb.password"),
}

app.config["CELERY_BROKER_URL"] = "redis://{username}:{password}@{host}:{port}/{db}".format(
    host=CONFIG.get("redis.host"),
    port=CONFIG.get("redis.port"),
    db=CONFIG.get("redis.db", 0),
    username=CONFIG.get("redis.username", ""),
    password=CONFIG.get("redis.password", ""),
)

app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_URL"] = app.config["CELERY_BROKER_URL"]
app.config["CACHE_DEFAULT_TIMEOUT"] = CONFIG.get("images_api.default_cache_times")


DB = MongoEngine(app)

REDIS = Cache(app)

CELERY = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
CELERY.conf.update(app.config)


@CELERY.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from . import scheduler

    sender.add_periodic_task(
        CONFIG.get("api.fetch_photos_delta"),
        scheduler.download_images.s(),
        name="Fetch photos",
    )
