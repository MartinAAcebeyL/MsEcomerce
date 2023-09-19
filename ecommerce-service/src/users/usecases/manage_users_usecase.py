from src.users.entities.user import User
from src.utils import utils

# Casos de uso para el manejo de users.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.


class ManageUsersUsecase:
    def __init__(self, users_repository):
        self.users_repository = users_repository

    def chance_role(self, id, role):
        self.users_repository.change_role_buyer(id, role)

    def get_users(self):
        # Retorna una lista de entidades User desde el repositorio.
        return self.users_repository.get_users()

    def get_user(self, user_id):
        # Retorna una instancia de user según la ID recibida.
        return self.users_repository.get_user(user_id)

    def create_user(self, data):
        # Crea una instancia User desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        user = User.from_dict(data)
        user = self.users_repository.create_user(user)
        return user

    def update_user(self, user_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        user = self.get_user(user_id)
        if user:
            data["updated_at"] = utils.get_current_datetime()
            user = self.users_repository.update_user(user_id, data)
            return user
        else:
            raise ValueError(f"User of ID {user_id} doesn't exist.")

    def delete_user(self, user_id):

        # Realiza un soft-delete del user con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        user = self.get_user(user_id)

        if user:
            data = {
                "deleted_at": utils.get_current_datetime()
            }
            user = self.users_repository.update_user(user_id, data)
        else:
            raise ValueError(
                f"User of ID {user_id} doesn't exist or is already deleted.")
