import os

from src.books.entities.book import Book

# Implementación con Firestore para el repositorio de libros.

class FirestoreBooksRepository():
    
    def __init__(self, firestore_client, test = False):

        # Obtener el nombre de la colección desde variables de entorno.
        # Si "test" es true, se le agrega un sufijo, útil para que 
        # las pruebas de integración no sobreescriban los datos existentes.

        self.test = test
        collection_name = os.environ["FIRESTORE_COLLECTION_NAME"]

        if test:
            collection_name += "_test"

        self.collection = firestore_client.collection(collection_name)

    def get_books(self, author = None, title = None, min_pages = None, max_pages = None):

        # Trae una lista de libros desde la colección de Firestore.
        # Al buscarlos, los transforma a entidad Book antes de retornarlos.
        # Opcionalmente puede recibir parámetros para filtrar por algún campo.

        results = self.collection.where("deleted_at", "==", None)

        if author:
            results = results.where("author", "==", author)

        if title:
            results = results.where("title", "==", title)

        if min_pages:
            results = results.where("pages", ">=", min_pages)

        if max_pages:
            results = results.where("pages", "<=", max_pages)

        books = []
        
        for document in results.stream():

            content = document.to_dict()
            content["id"] = document.id

            book = Book.from_dict(content)
            books.append(book)

        return books

    def get_book(self, book_id):

        content = self.collection.document(book_id).get().to_dict()

        if content and content.get("deleted_at") == None:

            content["id"] = book_id
            book = Book.from_dict(content)
            
            return book

        else:
            return None

    def create_book(self, book):

        content = book.to_dict()
        content.pop("id")

        document = self.collection.document()
        document.set(content)

        book.id = document.id
        
        return book

    def update_book(self, book_id, fields):

        # Actualiza la lista de campos recibida el documento especificado.

        document = self.collection.document(book_id).update(fields)
        return self.get_book(book_id)

    def hard_delete_book(self, book_id):

        # Hace un borrado real de un libro. Sólo usado durante tests.

        if self.test:
            self.collection.document(book_id).delete()

    def hard_delete_all_books(self):

        # Borra todos los libros de la colección. Sólo usado durante tests.

        if self.test:

            for document in self.collection.stream():
                self.hard_delete_book(document.id)