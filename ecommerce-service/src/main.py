from src.frameworks.db.redis import create_redis_client
from src.frameworks.http.flask import create_flask_app

from src.books.repositories.sqlalchemy_books_repository import SQLAlchemyBooksRepository
from src.books.usecases.manage_books_usecase import ManageBooksUsecase
from src.books.http.books_blueprint import create_books_blueprint

from src.greeting.http.greeting_blueprint import create_greeting_blueprint
from src.greeting.repositories.redis_greeting_cache import RedisGreetingCache
from src.greeting.usecases.greeting_usecase import GreetingUsecase

from src.users import user_blueprint
from src.transactions import transaction_blueprint
from src.products import product_blueprint
from src.categories import categorie_blueprint

from . import sqlalchemy_client

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

redis_client = create_redis_client()
redis_greeting_cache = RedisGreetingCache(redis_client)

# sqlalchemy instance

# repositories sqlachemy instances
sqlalchemy_books_repository = SQLAlchemyBooksRepository(
    sqlalchemy_client)


sqlalchemy_client.create_tables()

greeting_usecase = GreetingUsecase(redis_greeting_cache)
manage_books_usecase = ManageBooksUsecase(sqlalchemy_books_repository)


blueprints = [
    create_greeting_blueprint(greeting_usecase),
    create_books_blueprint(manage_books_usecase),
    user_blueprint,
    transaction_blueprint,
    product_blueprint,
    categorie_blueprint
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)
