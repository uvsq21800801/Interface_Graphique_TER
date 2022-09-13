# Schema de la table Motifs
schema = {
    "bsonType": "object",
    "required": [
        "color",
        "sign",
        "degre_min",
        "degre_max",
        "lst_v",
        "lst_b",
        "haveOW",
        "haveHbond",
    ],
    "properties": {
        "color": {
            "bsonType": "objectId",
            "description": "Point elements order for coloration",
        },
        "sign": {
            "bsonType": "string",
            "description": "Signature with coloration",
        },
        "nb_v": {"bsonType": "int", "description": "Number of vertex"},
        "nb_b": {"bsonType": "int", "description": "Number of bonds"},
        "degre_min": {
            "bsonType": "int",
            "minimum": 0,
            "description": "Degre of bonds minimum",
        },
        "degre_max": {
            "bsonType": "int",
            "description": "Degre of bonds maximum",
        },
        "lst_v": {
            "bsonType": "array",
            "items": {
                "bsonType": "string",
                "description": "Element of the vertex",
            },
            "description": "Vertex list",
        },
        "lst_b": {
            "bsonType": "array",
            "uniqueItems": True,
            "items": {
                "bsonType": "array",
                "minItems": 3,
                "maxItems": 3,
                "items": {
                    "bsonType": "int",
                    "minimum": 0,
                },
                "description": "[type, tail, head]",
            },
            "description": "Bonds list",
        },
        "haveOW": {
            "bsonType": "bool",
            "description": "True if there is water oxygen in vertex list",
        },
        "haveHbond": {
            "bsonType": "bool",
            "description": "True if there is H bond (2) in bond list",
        },
    },
}
