from flask import Blueprint, request
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.products.http.validation import product_validatable_fields
from src.utils.utils import jwt_required

# Endpoints para CRUD de PRODUCTS.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "product_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.


def create_products_blueprint(manage_products_usecase):
    blueprint = Blueprint("products", __name__)

    @blueprint.route("/products", methods=["GET"])
    @jwt_required()
    def get_products():
        products = manage_products_usecase.get_products()

        products_dict = []
        for product in products:
            products_dict.append(product.serialize())

        data = products_dict
        code = SUCCESS_CODE
        message = "Products obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/products/<string:product_id>", methods=["GET"])
    @jwt_required()
    def get_product(product_id):
        product = manage_products_usecase.get_product(product_id)

        if product:
            data = product.serialize()
            code = SUCCESS_CODE
            message = "Product obtained succesfully"
            http_code = 200
        else:
            data = None
            code = FAIL_CODE
            message = f"Product of ID {product_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/products", methods=["POST"])
    @jwt_required()
    @validate_schema_flask(product_validatable_fields.PRODUCT_CREATION_VALIDATABLE_FIELDS)
    def create_product():
        body = request.get_json()

        try:
            product = manage_products_usecase.create_product(body)
            data = product.serialize()
            code = SUCCESS_CODE
            message = "Product created succesfully"
            http_code = 201

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

    @blueprint.route("/products/<string:product_id>", methods=["PUT"])
    @jwt_required()
    @validate_schema_flask(product_validatable_fields.PRODUCT_UPDATE_VALIDATABLE_FIELDS)
    def update_product(product_id):
        body = request.get_json()

        try:
            product = manage_products_usecase.update_product(product_id, body)
            data = product.serialize()
            message = "Product updated succesfully"
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

    @blueprint.route("/products/<string:product_id>", methods=["DELETE"])
    @jwt_required()
    def delete_product(product_id):
        try:
            manage_products_usecase.delete_product(product_id)
            code = SUCCESS_CODE
            message = f"Product of ID {product_id} deleted succesfully."
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
