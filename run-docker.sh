#!/bin/bash

source bin/activate
uvicorn src/detective_catalog_service.service.server:app --host 0.0.0.0 --port 3003
