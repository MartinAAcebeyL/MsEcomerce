from .repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from .usecases.manage_users_usecase import ManageUsersUsecase
from .http.users_blueprint import create_users_blueprint

from src import sqlalchemy_client


sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)

manage_users_usecase = ManageUsersUsecase(sqlalchemy_users_repository)

user_blueprint = create_users_blueprint(manage_users_usecase)
