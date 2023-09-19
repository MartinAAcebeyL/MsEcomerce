from src import sqlalchemy_client
from .repositories.sqlalchemy_transactions_repository import SQLAlchemyTransactionsRepository
from .usecases.manage_transactions_usecase import ManageTransactionsUsecase
from .http.transaction_blueprint import create_transactions_blueprint


sqlalchemy_transactions_repository = SQLAlchemyTransactionsRepository(
    sqlalchemy_client)

manage_transactions_usecase = ManageTransactionsUsecase(
    sqlalchemy_transactions_repository)

transaction_blueprint = create_transactions_blueprint(
    manage_transactions_usecase)
