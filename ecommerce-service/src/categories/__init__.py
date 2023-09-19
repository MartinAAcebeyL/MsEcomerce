from .repositories.sqlalchemy_categories_repository import SQLAlchemyCategoriesRepository
from .usecases.manage_categories_usecase import ManageCategoriesUsecase
from .http.categories_blueprint import create_categories_blueprint

from src import sqlalchemy_client
sqlalchemy_categories_repository = SQLAlchemyCategoriesRepository(
    sqlalchemy_client)

manage_categories_usecase = ManageCategoriesUsecase(
    sqlalchemy_categories_repository)

categorie_blueprint = create_categories_blueprint(manage_categories_usecase)
