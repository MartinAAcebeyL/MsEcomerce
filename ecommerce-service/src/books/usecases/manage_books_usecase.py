from src.books.entities.book import Book
from src.utils import utils

# Casos de uso para el manejo de libros.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageBooksUsecase:

    def __init__(self, books_repository):
        self.books_repository = books_repository

    def get_books(self):

        # Retorna una lista de entidades Book desde el repositorio.

        return self.books_repository.get_books()

    def get_book(self, book_id):

        # Retorna una instancia de Book según la ID recibida.

        return self.books_repository.get_book(book_id)

    def create_book(self, data):

        # Crea una instancia Book desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        current_time = utils.get_current_datetime()
        
        data["created_at"] = current_time
        data["updated_at"] = current_time

        book = Book.from_dict(data)
        book = self.books_repository.create_book(book)

        return book

    def update_book(self, book_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        book = self.get_book(book_id)

        if book:

            data["updated_at"] = utils.get_current_datetime()
            book = self.books_repository.update_book(book_id, data)

            return book

        else:
            raise ValueError(f"Book of ID {book_id} doesn't exist.")

    def delete_book(self, book_id):

        # Realiza un soft-delete del libro con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        book = self.get_book(book_id)

        if book:

            data = {
                "deleted_at": utils.get_current_datetime()
            }
            
            book = self.books_repository.update_book(book_id, data)

        else:
            raise ValueError(f"Book of ID {book_id} doesn't exist or is already deleted.")