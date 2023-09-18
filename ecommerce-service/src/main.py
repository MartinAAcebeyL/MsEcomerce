from src.frameworks.db.redis import create_redis_client
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app


from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.users.usecases.manage_users_usecase import ManageUsersUsecase
from src.users.http.users_blueprint import create_users_blueprint

from src.products.repositories.sqlalchemy_products_repository import SQLAlchemyProductsRepository
from src.products.usecases.manage_products_usecase import ManageProductsUsecase
from src.products.http.products_blueprint import create_products_blueprint

from src.categories.repositories.sqlalchemy_categories_repository import SQLAlchemyCategoriesRepository
from src.categories.usecases.manage_categories_usecase import ManageCategoriesUsecase
from src.categories.http.categories_blueprint import create_categories_blueprint

from src.transactions.repositories.sqlalchemy_transactions_repository import SQLAlchemyTransactionsRepository
from src.transactions.usecases.manage_transactions_usecase import ManageTransactionsUsecase
from src.transactions.http.transaction_blueprint import create_transactions_blueprint

from src.greeting.http.greeting_blueprint import create_greeting_blueprint
from src.greeting.repositories.redis_greeting_cache import RedisGreetingCache
from src.greeting.usecases.greeting_usecase import GreetingUsecase

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

redis_client = create_redis_client()
redis_greeting_cache = RedisGreetingCache(redis_client)

# sqlalchemy instance
sqlalchemy_client = SQLAlchemyClient()

# repositories sqlachemy instances
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_products_repository = SQLAlchemyProductsRepository(
    sqlalchemy_client)
sqlalchemy_categories_repository = SQLAlchemyCategoriesRepository(
    sqlalchemy_client)
sqlalchemy_transactions_repository = SQLAlchemyTransactionsRepository(
    sqlalchemy_client)

sqlalchemy_client.create_tables()

greeting_usecase = GreetingUsecase(redis_greeting_cache)

manage_users_usecase = ManageUsersUsecase(sqlalchemy_users_repository)
manage_products_usecase = ManageProductsUsecase(sqlalchemy_products_repository)
manage_categories_usecase = ManageCategoriesUsecase(
    sqlalchemy_categories_repository)
manage_transactions_usecase = ManageTransactionsUsecase(
    sqlalchemy_transactions_repository)

blueprints = [
    create_greeting_blueprint(greeting_usecase),
    create_users_blueprint(manage_users_usecase),
    create_products_blueprint(manage_products_usecase),
    create_categories_blueprint(manage_categories_usecase),
    create_transactions_blueprint(manage_transactions_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)
