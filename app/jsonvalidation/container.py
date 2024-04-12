import jsonschema

create_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "vorlagen_id": {
            "type": "integer"
        },
        "connection_token": {
            "type": "string"
        },
        "port": {
            "type": "integer"
        },
        "volume_id": {
            "type": "integer"
        }
    },
    "required": ["name", "description", "vorlagen_id", "connection_token", "port", "volume_id"]
}


def validate_create(data):
    jsonschema.validate(data, schema=create_schema)
