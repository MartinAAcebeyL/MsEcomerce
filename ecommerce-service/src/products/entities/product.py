from src.utils.utils import format_date

# Entidad representando a un Product.


class Product():

    def __init__(self, id, name, description, quantity, status, seller_user, categories, transactions, created_at=None, updated_at=None, deleted_at=None):

        self.id = id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.status = status
        self.seller_user = seller_user
        self.categories = categories
        self.transactions = transactions

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "status": self.status,
            "seller_user": self.seller_user,
            "transactions": self.transactions,
            "categories": self.categories,

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
        description = dict.get("description")
        quantity = dict.get("quantity")
        status = dict.get("status")
        seller_user = dict.get("seller_user")
        transactions = dict.get("transactions")
        categories = dict.get("categories")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Product(id, name, description, quantity, status, seller_user, transactions, categories, created_at, updated_at, deleted_at)
