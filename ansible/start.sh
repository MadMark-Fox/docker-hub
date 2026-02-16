#!/bin/bash

# Iniciar Nginx en segundo plano
nginx

# Iniciar Gunicorn con workers Uvicorn (en primer plano)
cd /opt/ansible-visual/api
/opt/ansible-visual/api/venv/bin/gunicorn main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
