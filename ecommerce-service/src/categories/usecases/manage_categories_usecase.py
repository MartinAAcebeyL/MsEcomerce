from src.categories.entities.category import Category
from src.utils import utils

# Casos de uso para el manejo de libros.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageCategoriesUsecase:

    def __init__(self, categories_repository):
        self.categories_repository = categories_repository

    def get_categories(self):

        # Retorna una lista de entidades Category desde el repositorio.

        return self.categories_repository.get_categories()

    def get_category(self, category_id):

        # Retorna una instancia de Category según la ID recibida.

        return self.categories_repository.get_category(category_id)

    def create_category(self, data):

        # Crea una instancia Category desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        current_time = utils.get_current_datetime()
        
        data["created_at"] = current_time
        data["updated_at"] = current_time

        category = Category.from_dict(data)
        category = self.categories_repository.create_category(category)

        return category

    def update_category(self, category_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        category = self.get_category(category_id)

        if category:

            data["updated_at"] = utils.get_current_datetime()
            category = self.categories_repository.update_category(category_id, data)

            return category

        else:
            raise ValueError(f"Category of ID {category_id} doesn't exist.")

    def delete_category(self, category_id):

        # Realiza un soft-delete del libro con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        category = self.get_category(category_id)

        if category:

            data = {
                "deleted_at": utils.get_current_datetime()
            }
            
            category = self.categories_repository.update_category(category_id, data)

        else:
            raise ValueError(f"Category of ID {category_id} doesn't exist or is already deleted.")