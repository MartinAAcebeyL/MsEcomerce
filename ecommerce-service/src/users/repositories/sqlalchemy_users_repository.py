from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP, Boolean
from src.users.entities.user import User

# Implementación con SQL Alchemy para el repositorio de libros.


class SQLAlchemyUsersRepository:
    def __init__(self, sqlalchemy_client, test=False):
        # Mapear la tabla User de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.
        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Users"

        if test:
            table_name += "_test"

        self.users_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("email", String(50)),
            Column("password", String(50)),
            Column("is_admin", Boolean),
            Column("is_buyer", Boolean),
            Column("is_seller", Boolean),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            User, self.users_table)

    def get_user_by_email(self, email):
        with self.session_factory() as session:
            user = session.query(User).filter_by(
                email=email, deleted_at=None).first()
            return user

    def change_role(self, id: int, role: str, value: bool) -> None:
        with self.session_factory() as session:
            user = self.get_user(id)

            if user:
                if role == "buyer":
                    session.query(User).filter_by(
                        id=id, deleted_at=None).update({
                            "is_buyer": value
                        }
                    )
                else:
                    session.query(User).filter_by(
                        id=id, deleted_at=None).update({
                            "is_seller": value
                        }
                    )
                session.commit()

    def get_users_by_role(self, role: str):
        users = None
        with self.session_factory() as session:
            if role == 'buyer':
                users = session.query(User).filter_by(
                    is_buyer=True, deleted_at=None).all()
            else:
                users = session.query(User).filter_by(
                    is_seller=True, deleted_at=None).all()
        return users

    def get_users(self):
        with self.session_factory() as session:
            users = session.query(User).filter_by(deleted_at=None).all()
            return users

    def get_user(self, id):
        with self.session_factory() as session:
            user = session.query(User).filter_by(
                id=id, deleted_at=None).first()
            return user

    def create_user(self, user):
        with self.session_factory() as session:
            session.add(user)
            session.commit()
            return user

    def update_user(self, id, fields):
        # Actualiza sólo los campos de la lista "fields" del user especificado.
        # Luego retorna el user con los nuevos datos.

        with self.session_factory() as session:
            session.query(User).filter_by(
                id=id, deleted_at=None).update(fields)
            session.commit()
            user = session.query(User).filter_by(
                id=id, deleted_at=None).first()
            return user

    def hard_delete_user(self, id):
        with self.session_factory() as session:
            user = session.query(User).get(id)
            session.delete(user)
            session.commit()

    def hard_delete_all_users(self):
        if self.test:
            with self.session_factory() as session:
                session.query(User).delete()
                session.commit()

    def drop_users_table(self):
        if self.test:
            self.client.drop_table(self.users_table)
