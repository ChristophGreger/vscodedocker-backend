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
        "vscodeextension": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "installcommands": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["name", "description", "vscodeextension", "installcommands"]

}

edit_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "vscodeextension": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "installcommands": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "version": {
            "type": "integer"
        }
    },
    "required": ["name", "description", "vscodeextension", "installcommands", "version"]
}


def validate_create(data):
    jsonschema.validate(data, create_schema)


def validate_edit(data):
    jsonschema.validate(data, edit_schema)
