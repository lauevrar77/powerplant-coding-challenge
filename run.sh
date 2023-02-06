#!/bin/sh

./.venv/bin/gunicorn --bind=0.0.0.0:8888 --worker-class=gevent --worker-connections=1000 --workers=3 wsgi
