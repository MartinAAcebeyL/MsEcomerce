# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un Product. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

PRODUCT_CREATION_VALIDATABLE_FIELDS = {
    "name": {
        "required": True,
        "type": "string",
    },
    "description": {
        "required": True,
        "type": "string",
    },
    "quantity": {
        "required": True,
        "type": "integer",
    },
    "status": {
        "required": False,
        "type": "integer",
    },
    "seller_user": {
        "required": True,
        "type": "integer",
    },
    "transactions": {
        "required": False,
        "type": "integer",
    },
    "categories": {
        "required": True,
        "type": "integer",
    },
}

PRODUCT_UPDATE_VALIDATABLE_FIELDS = {
    "name": {
        "required": False,
        "type": "string",
    },
    "description": {
        "required": False,
        "type": "string",
    },
    "quantity": {
        "required": False,
        "type": "integer",
    },
    "status": {
        "required": False,
        "type": "integer",
    },
    "transactions": {
        "required": False,
        "type": "integer",
    },
    "categories": {
        "required": False,
        "type": "integer",
    },
}
