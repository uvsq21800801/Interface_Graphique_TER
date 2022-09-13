# Schema de la table Colorations
schema = {
    "bsonType": "object",
    "required": ["name", "elements", "haveH"],
    "properties": {
        "name": {"bsonType": "string"},
        "elements": {
            "bsonType": "array",
            "uniqueItems": True,
            "items": {"bsonType": "string"},
        },
        "haveH": {"bsonType": "bool"},
    },
}
