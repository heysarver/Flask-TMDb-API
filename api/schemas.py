SEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        }
    },
    "required": ["query"]
}

ACTOR_FILTER_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "min_popularity": {
            "type": "number",
            "minimum": 0
        },
        "gender": {
            "type": "integer",
            "enum": [0, 1, 2, 3]  # 0: not specified, 1: female, 2: male, 3: non-binary
        },
        "birth_year_from": {
            "type": "integer",
            "minimum": 1800
        },
        "birth_year_to": {
            "type": "integer",
            "minimum": 1800
        }
    },
    "required": ["query"]
}

MEDIA_FILTER_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "year": {
            "type": "integer",
            "minimum": 1900
        },
        "genre_id": {
            "type": "integer",
            "minimum": 1
        },
        "min_rating": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
        },
        "language": {
            "type": "string",
            "pattern": "^[a-zA-Z]{2}$"
        }
    },
    "required": ["query"]
}
