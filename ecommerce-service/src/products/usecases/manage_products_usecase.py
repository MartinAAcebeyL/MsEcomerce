from src.products.entities.product import Product
from src.utils import utils
from src.users import sqlalchemy_users_repository
# Casos de uso para el manejo de Products.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.


class ManageProductsUsecase:
    def __init__(self, products_repository):
        self.products_repository = products_repository

    def get_products(self):
        # Retorna una lista de entidades Product desde el repositorio.
        return self.products_repository.get_products()

    def get_product(self, product_id):
        # Retorna una instancia de Product según la ID recibida.
        return self.products_repository.get_product(product_id)

    def create_product(self, data):
        # Crea una instancia Product desde la data recibida, que ya debe venir validada desde afuera, y guarda dicha instancia en el repositorio para finalmente retornarla.

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        product = Product.from_dict(data)
        product = self.products_repository.create_product(product)
        if self.products_repository.count_registry_by_seller_user(product.seller_user) == 1:
            sqlalchemy_users_repository.change_role(
                product.seller_user, "seller", True)
        return product

    def update_product(self, product_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        product = self.get_product(product_id)

        if product:

            data["updated_at"] = utils.get_current_datetime()
            product = self.products_repository.update_product(product_id, data)

            return product

        else:
            raise ValueError(f"Product of ID {product_id} doesn't exist.")

    def delete_product(self, product_id):

        # Realiza un soft-delete del libro con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        product = self.get_product(product_id)

        if product:
            data = {
                "deleted_at": utils.get_current_datetime()
            }
            product = self.products_repository.update_product(product_id, data)
        else:
            raise ValueError(
                f"Product of ID {product_id} doesn't exist or is already deleted.")
