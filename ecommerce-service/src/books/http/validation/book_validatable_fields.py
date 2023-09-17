# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

BOOK_CREATION_VALIDATABLE_FIELDS = {

    "title": {
        "required": True,
        "type": "string",
    },

    "author": {
        "required": True,
        "type": "string",
    },

    "pages": {
        "required": True,
        "type": "integer",
    },

}

BOOK_UPDATE_VALIDATABLE_FIELDS = {

    "title": {
        "required": False,
        "type": "string",
    },

    "author": {
        "required": False,
        "type": "string",
    },

    "pages": {
        "required": False,
        "type": "integer",
    },

}