# Schema de la table Similarities
schema = {
    "bsonType": "object",
    "required": ["motif1", "motif2", "values"],
    "properties": {
        "motif1": {"bsonType": "objectId"},
        "motif2": {"bsonType": "objectId"},
        "values": {
            "bsonType": "array",
            "minItems": 4,
            "items": {
                "bsonType": "double"
            }
        },
    },
}