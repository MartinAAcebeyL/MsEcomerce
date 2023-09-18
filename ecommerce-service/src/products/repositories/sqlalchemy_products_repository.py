from src.products.entities.product import Product
from src.categories.entities.category import Category
from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

# Implementación con SQL Alchemy para el repositorio de Products.


class SQLAlchemyProductsRepository():
    def __init__(self, sqlalchemy_client, test=False):
        # Mapear la tabla Product de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Products"

        if test:
            table_name += "_test"

        self.products_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(150)),
            Column("description", String(150)),
            Column("quantity", Integer),
            Column("status", String(150)),
            Column("seller_user", Integer, ForeignKey("Users.id")),
            Column("transactions", Integer),
            Column("categories", Integer),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Product, self.products_table)
        Product.seller_user = relationship(
            "User", back_populates="seller_user")
        Product.categories = relationship(
            "Category", back_populates="products", secondary="product_category_association")

    def get_products(self):
        with self.session_factory() as session:
            products = session.query(Product).filter_by(deleted_at=None).all()
            return products

    def get_product(self, id):
        with self.session_factory() as session:
            product = session.query(Product).filter_by(
                id=id, deleted_at=None).first()
            return product

    def create_product(self, product):
        with self.session_factory() as session:
            session.add(product)
            session.commit()
            return product

    def update_product(self, id, fields):
        # Actualiza sólo los campos de la lista "fields" en el libro especificado.
        # Luego retorna el libro con los nuevos datos.

        with self.session_factory() as session:
            session.query(Product).filter_by(
                id=id, deleted_at=None).update(fields)
            session.commit()
            product = session.query(Product).filter_by(
                id=id, deleted_at=None).first()
            return product

    def hard_delete_product(self, id):
        with self.session_factory() as session:
            product = session.query(Product).get(id)
            session.delete(product)
            session.commit()

    def hard_delete_all_products(self):
        if self.test:
            with self.session_factory() as session:
                session.query(Product).delete()
                session.commit()

    def drop_products_table(self):
        if self.test:
            self.client.drop_table(self.products_table)
