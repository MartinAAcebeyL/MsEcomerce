from flask import Blueprint, request
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.categories.http.validation import category_validatable_fields
from src.utils.utils import jwt_required
# Endpoints para CRUD de Categories.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "category_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.


def create_categories_blueprint(manage_categories_usecase):
    blueprint = Blueprint("categories", __name__)

    @blueprint.route("/categories", methods=["GET"])
    @jwt_required()
    def get_categories():
        categories = manage_categories_usecase.get_categories()

        categories_dict = []
        for category in categories:
            categories_dict.append(category.serialize())

        data = categories_dict
        code = SUCCESS_CODE
        message = "Categories obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/categories/<string:category_id>", methods=["GET"])
    @jwt_required()
    def get_category(category_id):

        category = manage_categories_usecase.get_category(category_id)

        if category:
            data = category.serialize()
            code = SUCCESS_CODE
            message = "Category obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Category of ID {category_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/categories", methods=["POST"])
    @jwt_required()
    @validate_schema_flask(category_validatable_fields.CATEGORY_CREATION_VALIDATABLE_FIELDS)
    def create_category():
        body = request.get_json()
        try:
            category = manage_categories_usecase.create_category(body)
            data = category.serialize()
            code = SUCCESS_CODE
            message = "Category created succesfully"
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

    @blueprint.route("/categories/<string:category_id>", methods=["PUT"])
    @jwt_required()
    @validate_schema_flask(category_validatable_fields.CATEGORY_UPDATE_VALIDATABLE_FIELDS)
    def update_category(category_id):

        body = request.get_json()

        try:
            category = manage_categories_usecase.update_category(
                category_id, body)
            data = category.serialize()
            message = "Category updated succesfully"
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

    @blueprint.route("/categories/<string:category_id>", methods=["DELETE"])
    @jwt_required(roles=["admin"])
    def delete_category(category_id):

        try:
            manage_categories_usecase.delete_category(category_id)
            code = SUCCESS_CODE
            message = f"Category of ID {category_id} deleted succesfully."
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
