#!/bin/sh

source venv/bin/activate
uvicorn detective_catalog_service.service.server:app --host 0.0.0.0 --port 3003
