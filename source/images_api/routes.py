from flask import Response, jsonify

from . import REDIS, CONFIG, app
from .models import Image


@app.route("/search/<search_term>")
@REDIS.memoize(CONFIG.get("api.search_cache_time"))
def search(search_term):
    app.logger.info("Received search term: " + search_term)
    images = Image.objects.search_text(search_term)
    return Response(status=404)\
        if images.count() == 0 else Response(images.to_json(), content_type="application/json")
