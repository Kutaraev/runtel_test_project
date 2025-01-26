animal_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["type", "name", "age"],
}
