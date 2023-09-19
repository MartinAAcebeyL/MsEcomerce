from src.transactions.entities.transaction import Transaction
from src.utils import utils
from src.users import sqlalchemy_users_repository
from src.products import sqlalchemy_products_repository
# Casos de uso para el manejo de Transactions.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.


class ManageTransactionsUsecase:
    def __init__(self, transactions_repository):
        self.transactions_repository = transactions_repository

    def get_transactions(self):
        # Retorna una lista de entidades Transaction desde el repositorio.
        return self.transactions_repository.get_transactions()

    def get_transaction(self, transaction_id):
        # Retorna una instancia de Transaction según la ID recibida.
        return self.transactions_repository.get_transaction(transaction_id)

    def create_transaction(self, data):
        # Crea una instancia transaction desde la data recibida, que ya debe venir validada desde afuera, y guarda dicha instancia en el repositorio para finalmente retornarla.

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        transaction = Transaction.from_dict(data)
        if sqlalchemy_products_repository.register_sale(
                transaction.amount, transaction.products):
            transaction = self.transactions_repository.create_transaction(
                transaction)

            if self.transactions_repository.count_registry_by_buyer_user(transaction.buyer_user) == 1:
                sqlalchemy_users_repository.change_role(
                    transaction.buyer_user, "buyer", True)

            return transaction
        return False

    def update_transaction(self, transaction_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        transaction = self.get_transaction(transaction_id)

        if transaction:
            data["updated_at"] = utils.get_current_datetime()
            transaction = self.transactions_repository.update_transaction(
                transaction_id, data)

            return transaction

        else:
            raise ValueError(
                f"Transaction of ID {transaction_id} doesn't exist.")

    def delete_transaction(self, transaction_id):

        # Realiza un soft-delete del libro con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        transaction = self.get_transaction(transaction_id)

        if transaction:
            sqlalchemy_products_repository.return_sale(
                amount=transaction.amount, id=transaction.products)
            
            data = {
                "deleted_at": utils.get_current_datetime()
            }
            
            transaction = self.transactions_repository.update_transaction(
                transaction_id, data)
        else:
            raise ValueError(
                f"Transaction of ID {transaction_id} doesn't exist or is already deleted.")
