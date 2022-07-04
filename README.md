# detective Catalog-Service

![CI Pipeline](https://github.com/detective-solutions/detective-catalog-service/actions/workflows/ci.yml/badge.svg)

Microservice to insert, update, list or delete catalogs in Trino.

To start service locally run:

`uvicorn src.detective_catalog_service.service.server:app --reload --port 3000`
