# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un Product. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

TRANSACTION_CREATION_VALIDATABLE_FIELDS = {
    "buyer_user": {
        "required": True,
        "type": "integer",
    },
    "products": {
        "required": True,
        "type": "integer",
    },
    "amount": {
        "required": True,
        "type": "integer",
    },
}

TRANSACTION_UPDATE_VALIDATABLE_FIELDS = {
    "buyer_user": {
        "required": False,
        "type": "integer",
    },
    "products": {
        "required": False,
        "type": "integer",
    },
    "amount": {
        "required": False,
        "type": "integer",
    },
}
