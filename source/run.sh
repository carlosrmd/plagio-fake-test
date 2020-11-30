echo "Running server..."
gunicorn -c python:images_api.wsgi app_server:app