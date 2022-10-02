from detective_catalog_service.service.models.response.catalog_requests import CatalogDefinitionResponse, \
    CatalogProperty

excluded_property = ["sourceConnectionName"]


def transform_model_response(model: dict) -> CatalogDefinitionResponse:

    required = model["required"]

    result = CatalogDefinitionResponse(
        connectorType=model["title"].lower(),
        properties=list()
    )

    for key, prop_set in model["properties"].items():
        if key != "connectorName":
            prop = CatalogProperty(
                propertyName=key,
                displayName=prop_set.get('title', key),
                description=prop_set.get("description", ""),
                default=prop_set.get("default", ""),
                type=prop_set.get("type", ""),
                required=True if key in required else False
            )
            result.properties.append(prop)

    return result
