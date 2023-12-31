from .repositories.sqlalchemy_products_repository import SQLAlchemyProductsRepository
from .usecases.manage_products_usecase import ManageProductsUsecase
from .http.products_blueprint import create_products_blueprint

from src import sqlalchemy_client

sqlalchemy_products_repository = SQLAlchemyProductsRepository(
    sqlalchemy_client)

manage_products_usecase = ManageProductsUsecase(sqlalchemy_products_repository)

product_blueprint = create_products_blueprint(manage_products_usecase)
