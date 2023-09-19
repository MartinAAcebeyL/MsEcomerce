from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from src.categories.entities.category import Category
    
# Implementación con SQL Alchemy para el repositorio de categories.

class SQLAlchemyCategoriesRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Category de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Categories"

        if test:
            table_name += "_test"

        self.categories_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("name", String(150)),
            Column("description", String(150)),
            Column("products", Integer),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable = True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Category, self.categories_table)

    def get_categories(self):
        
        with self.session_factory() as session:
            
            categories = session.query(Category).filter_by(deleted_at = None).all()
            return categories

    def get_category(self, id):
        
        with self.session_factory() as session:

            category = session.query(Category).filter_by(id = id, deleted_at = None).first()
            return category

    def create_category(self, category):

        with self.session_factory() as session:

            session.add(category)
            session.commit()

            return category

    def update_category(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el libro especificado.
        # Luego retorna el libro con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Category).filter_by(id = id, deleted_at = None).update(fields)
            session.commit()
            
            category = session.query(Category).filter_by(id = id, deleted_at = None).first()
            return category

    def hard_delete_category(self, id):

        with self.session_factory() as session:

            category = session.query(Category).get(id)
            session.delete(category)
            session.commit()

    def hard_delete_all_categories(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Category).delete()
                session.commit()

    def drop_categories_table(self):

        if self.test:
            self.client.drop_table(self.categories_table)