from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP

from src.books.entities.book import Book
    
# Implementación con SQL Alchemy para el repositorio de libros.

class SQLAlchemyBooksRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Book de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Books"

        if test:
            table_name += "_test"

        self.books_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("title", String(50)),
            Column("author", String(50)),
            Column("pages", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable = True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Book, self.books_table)

    def get_books(self):
        
        with self.session_factory() as session:
            
            books = session.query(Book).filter_by(deleted_at = None).all()
            return books

    def get_book(self, id):
        
        with self.session_factory() as session:

            book = session.query(Book).filter_by(id = id, deleted_at = None).first()
            return book

    def create_book(self, book):

        with self.session_factory() as session:

            session.add(book)
            session.commit()

            return book

    def update_book(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el libro especificado.
        # Luego retorna el libro con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Book).filter_by(id = id, deleted_at = None).update(fields)
            session.commit()
            
            book = session.query(Book).filter_by(id = id, deleted_at = None).first()
            return book

    def hard_delete_book(self, id):

        with self.session_factory() as session:

            book = session.query(Book).get(id)
            session.delete(book)
            session.commit()

    def hard_delete_all_books(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Book).delete()
                session.commit()

    def drop_books_table(self):

        if self.test:
            self.client.drop_table(self.books_table)