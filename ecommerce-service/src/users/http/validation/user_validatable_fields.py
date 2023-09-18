USER_CREATION_VALIDATABLE_FIELDS = {
    "name": {
        "required": True,
        "type": "string",
    },

    "email": {
        "required": True,
        "type": "string",
    },

    "password": {
        "required": True,
        "type": "string",
    },
    "is_admin": {
        "required": True,
        "type": "boolean",
    }

}

USER_UPDATE_VALIDATABLE_FIELDS = {
    "name": {
        "required": False,
        "type": "string",
    },

    "email": {
        "required": False,
        "type": "string",
    },

    "password": {
        "required": False,
        "type": "string",
    },
}
