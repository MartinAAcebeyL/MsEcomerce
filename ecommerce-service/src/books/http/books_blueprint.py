from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.books.http.validation import book_validatable_fields

# Endpoints para CRUD de libros.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "book_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_books_blueprint(manage_books_usecase):

    blueprint = Blueprint("books", __name__)

    @blueprint.route("/books", methods = ["GET"])
    def get_books():

        books = manage_books_usecase.get_books()

        books_dict = []
        for book in books:
            books_dict.append(book.serialize())

        data = books_dict
        code = SUCCESS_CODE
        message = "Books obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code

    @blueprint.route("/books/<string:book_id>", methods = ["GET"])
    def get_book(book_id):

        book = manage_books_usecase.get_book(book_id)

        if book:
            data = book.serialize()
            code = SUCCESS_CODE
            message = "Book obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Book of ID {book_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code

    @blueprint.route("/books", methods = ["POST"])
    @validate_schema_flask(book_validatable_fields.BOOK_CREATION_VALIDATABLE_FIELDS)
    def create_book():

        body = request.get_json()

        try:
            book = manage_books_usecase.create_book(body)
            data = book.serialize()
            code = SUCCESS_CODE
            message = "Book created succesfully"
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

    @blueprint.route("/books/<string:book_id>", methods = ["PUT"])
    @validate_schema_flask(book_validatable_fields.BOOK_UPDATE_VALIDATABLE_FIELDS)
    def update_book(book_id):

        body = request.get_json()

        try:
            book = manage_books_usecase.update_book(book_id, body)
            data = book.serialize()
            message = "Book updated succesfully"
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

    @blueprint.route("/books/<string:book_id>", methods = ["DELETE"])
    def delete_book(book_id):

        try:
            manage_books_usecase.delete_book(book_id)
            code = SUCCESS_CODE
            message = f"Book of ID {book_id} deleted succesfully."
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
