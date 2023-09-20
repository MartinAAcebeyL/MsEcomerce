from src.users import sqlalchemy_users_repository
from src.users.entities.user import User

from src.categories import sqlalchemy_categories_repository
from src.categories.entities.category import Category

from src.products import sqlalchemy_products_repository
from src.products.entities.product import Product

from src.transactions import sqlalchemy_transactions_repository
from src.transactions.entities.transaction import Transaction

from src.utils.utils import get_current_datetime
from faker import Faker

fake = Faker()
current_time = get_current_datetime()


def create_users():
    for _ in range(10):
        data = {
            "name": fake.name(),
            "email": fake.email(),
            "password": "123456",
            "is_admin": fake.random_element(elements=(False, True))
        }

        data["created_at"] = current_time
        data["updated_at"] = current_time

        user = User.from_dict(data)

        sqlalchemy_users_repository.create_user(user)


def create_categories():
    for _ in range(20):
        data = {
            "name": fake.name(),
            "description": fake.paragraph(nb_sentences=2)
        }
        data["created_at"] = current_time
        data["updated_at"] = current_time
        category = Category.from_dict(data)
        sqlalchemy_categories_repository.create_category(category)


def create_products():
    for _ in range(20):
        data = {
            "name": fake.name(),
            "description": fake.paragraph(nb_sentences=2),
            "quantity": fake.random_int(min=100, max=250),
            "status": "activo",
            "seller_user": fake.random_int(min=1, max=10),
            "categories": fake.random_int(min=1, max=20),
        }
        data["created_at"] = current_time
        data["updated_at"] = current_time
        product = Product.from_dict(data)
        sqlalchemy_products_repository.create_product(product)


def create_transactions():
    for _ in range(5):
        data = {
            "buyer_user": fake.random_int(min=1, max=10),
            "products": fake.random_int(min=1, max=20),
            "amount": fake.random_int(min=1, max=20),
        }
        data["created_at"] = current_time
        data["updated_at"] = current_time
        transaction = Transaction.from_dict(data)
        sqlalchemy_transactions_repository.create_transaction(transaction)


def main():
    create_users()
    create_categories()
    create_products()
    create_transactions()


if __name__ == "__main__":
    main()
