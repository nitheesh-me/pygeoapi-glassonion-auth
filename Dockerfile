FROM geopython/pygeoapi:latest

COPY --chown=root:root docker/entrypoint.sh /entrypoint.sh

RUN pip install Flask-Authorize Flask-login Flask-Dance
COPY pygeoapi_secure /app/pygeoapi_secure

RUN chmod +x /entrypoint.sh
