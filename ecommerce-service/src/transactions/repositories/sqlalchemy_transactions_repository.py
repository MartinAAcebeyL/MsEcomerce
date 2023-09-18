from src.products.entities.product import Product
from src.users.entities.user import User
from src.transactions.entities.transaction import Transaction
from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

# Implementación con SQL Alchemy para el repositorio de Transactions.


class SQLAlchemyTransactionsRepository():
    def __init__(self, sqlalchemy_client, test=False):
        # Mapear la tabla Transaction de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Transactions"

        if test:
            table_name += "_test"

        self.products_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("buyer_user", Integer, ForeignKey("Users.id")),
            Column("products", Integer),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Transaction, self.products_table)
        Transaction.buyer_user = relationship(
            "User", back_populates="buyer_user")
        Transaction.products = relationship(
            "Products", back_populates="products", secondary="transaction_product_association")

    def get_transactions(self):
        with self.session_factory() as session:
            transactions = session.query(
                Transaction).filter_by(deleted_at=None).all()
            return transactions

    def get_transaction(self, id):
        with self.session_factory() as session:
            transaction = session.query(Transaction).filter_by(
                id=id, deleted_at=None).first()
            return transaction

    def create_transaction(self, transaction):
        with self.session_factory() as session:
            session.add(transaction)
            session.commit()
            return transaction

    def update_transaction(self, id, fields):
        # Actualiza sólo los campos de la lista "fields" en el Transaction especificado.
        # Luego retorna el Transaction con los nuevos datos.

        with self.session_factory() as session:
            session.query(Transaction).filter_by(
                id=id, deleted_at=None).update(fields)
            session.commit()
            transaction = session.query(Transaction).filter_by(
                id=id, deleted_at=None).first()
            return transaction

    def hard_delete_transaction(self, id):
        with self.session_factory() as session:
            transaction = session.query(Transaction).get(id)
            session.delete(transaction)
            session.commit()

    def hard_delete_all_transactions(self):
        if self.test:
            with self.session_factory() as session:
                session.query(Transaction).delete()
                session.commit()

    def drop_transactions_table(self):
        if self.test:
            self.client.drop_table(self.transactions_table)
