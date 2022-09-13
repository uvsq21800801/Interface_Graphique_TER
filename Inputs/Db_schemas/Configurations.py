# Schema de la table Configurations
schema = {
    "bsonType": "object",
    "required": ["struct", "color", "number", "sizes"],
    "properties": {
        "struct": {"bsonType": "objectId"},
        "color": {"bsonType": "objectId"},
        "number": {"bsonType": "int", "minimum": 0},
        "repetiton": {"bsonType": "int", "minimum": 1},
        "sizes": {
            "bsonType": "array",
            "uniqueItems": True,
            "items": {"bsonType": "int"},
        },
    },
}
