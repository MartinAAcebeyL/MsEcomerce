from src.utils.utils import format_date

# Entidad representando a un user.


class User:
    def __init__(self, id, name, email, password, is_admin,
                 created_at=None, updated_at=None, deleted_at=None):

        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_seller = False
        self.is_buyer = False

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
            "is_seller": self.is_seller,
            "is_buyer": self.is_buyer,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):
        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict()

        data.pop("deleted_at")
        data.pop("password")

        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])

        return data

    @classmethod
    def from_dict(cls, dict):
        # Retorna una instancia de este objeto desde un diccionario de datos,
        # para no tener que llamar al constructor pasando los datos uno a uno.
        # Si un campo falta en el diccionario, se asume valor None.

        id = dict.get("id")
        name = dict.get("name")
        email = dict.get("email")
        password = dict.get("password")
        is_admin = dict.get("is_admin")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return User(id, name, email, password, is_admin, created_at, updated_at, deleted_at)
