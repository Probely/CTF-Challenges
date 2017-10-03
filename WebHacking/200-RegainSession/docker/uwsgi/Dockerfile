FROM python:3.6-jessie

ADD ./src/requirements.txt /

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
RUN set -ex \
    && python3 -m venv /venv \
    && /venv/bin/pip install -U pip \
    && UWSGI_PROFILE=gevent /venv/bin/pip install -U uwsgi \
    && /venv/bin/pip install --no-cache-dir -r /requirements.txt

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
ADD ./src /code
WORKDIR /code
RUN ls /code

# uWSGI will listen on this port
EXPOSE 8000

# uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv UWSGI_HTTP=:8000 \
    UWSGI_MASTER=1 UWSGI_WORKERS=4 \
    UWSGI_WSGI_ENV_BEHAVIOR=holy UWSGI_VACUUM=1

# Start uWSGI
CMD ["/venv/bin/uwsgi", "--gevent", "100", "--file", "app.py"]

