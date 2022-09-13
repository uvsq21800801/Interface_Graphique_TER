# Schema de la table Structures
schema = {
    "bsonType": "object",
    "required": ["name", "colors"],
    "properties": {
        "name": {"bsonType": "string"},
        "colors": {
            "bsonType": "array",
            "uniqueItems": True,
            "items": {"bsonType": "objectId"},
        },
    },
}
