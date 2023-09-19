from flask import Blueprint, request
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.transactions.http.validation import transaction_validatable_fields
# Endpoints para CRUD de TRANSACTION.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "transaction_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.


def create_transactions_blueprint(manage_transactions_usecase):
    blueprint = Blueprint("transactions", __name__)

    @blueprint.route("/transactions", methods=["GET"])
    def get_transactions():
        transactions = manage_transactions_usecase.get_transactions()

        transactions_dict = []
        for product in transactions:
            transactions_dict.append(product.serialize())

        data = transactions_dict
        code = SUCCESS_CODE
        message = "Transaction obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/transacions/<string:transacion_id>", methods=["GET"])
    def get_transacion(transacion_id):
        transacion = manage_transactions_usecase.get_transacion(transacion_id)

        if transacion:
            data = transacion.serialize()
            code = SUCCESS_CODE
            message = "transacion obtained succesfully"
            http_code = 200
        else:
            data = None
            code = FAIL_CODE
            message = f"transacion of ID {transacion_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/transactions", methods=["POST"])
    @validate_schema_flask(transaction_validatable_fields.TRANSACTION_CREATION_VALIDATABLE_FIELDS)
    def create_transaction():
        body = request.get_json()

        try:
            transaction = manage_transactions_usecase.create_transaction(body)
            if not transaction:
                raise Exception(
                    "You cannot create a transaction with a quantity greater than stock")
            data = transaction.serialize()
            code = SUCCESS_CODE
            message = "Transaction created succesfully"
            http_code = 201
        except Exception as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400
        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/transactions/<string:transaction_id>", methods=["PUT"])
    @validate_schema_flask(transaction_validatable_fields.TRANSACTION_UPDATE_VALIDATABLE_FIELDS)
    def update_transaction(transaction_id):
        body = request.get_json()

        try:
            transaction = manage_transactions_usecase.update_transaction(
                transaction_id, body)
            data = transaction.serialize()
            message = "Transaction updated succesfully"
            code = SUCCESS_CODE
            http_code = 200
        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/transactions/<string:transaction_id>", methods=["DELETE"])
    def delete_transaction(transaction_id):
        try:
            manage_transactions_usecase.delete_transaction(transaction_id)
            code = SUCCESS_CODE
            message = f"Transaction of ID {transaction_id} deleted succesfully."
            http_code = 200
        except ValueError as e:
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        return response, http_code

    return blueprint
