# Schema de la table Occurrences
schema = {
    "bsonType": "object",
    "required": ["struct", "color", "config", "motif", "repetition"],
    "properties": {
        "struct": {"bsonType": "objectId"},
        "color": {"bsonType": "objectId"},
        "config": {"bsonType": "objectId"},
        "motif": {"bsonType": "objectId"},
        "repetition": {"bsonType": "int", "minimum": 1},
        "cover_rate": {
            "bsonType": "double",
            "minimum": 1.0,
        },
        "distr_rate": {
            "bsonType": "double",
            "minimum": 0.0,
            "maximum": 1.0,
        },
    },
}
