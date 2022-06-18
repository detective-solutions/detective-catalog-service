
def transform_model_response(model: dict) -> dict:
    required = model["required"]
    result = {"title": model["title"], "properties": list()}
    for key, prop_set in model["properties"].items():
        result["properties"].append({
            "propertyName": key,
            "displayName": prop_set.get('title', key),
            "description": prop_set.get("description", ""),
            "default": prop_set.get("default", ""),
            "type": prop_set.get("type", ""),
            "required": True if key in required else False
        })
    return result
