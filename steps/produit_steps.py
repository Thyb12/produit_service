import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from behave import given, when, then
from api.produit_api import create_produit, read_produits, delete_produit, read_specific_produit
from unittest.mock import patch

# Configuration de la base de données en fonction de la variable d'environnement ENV
if os.environ.get("ENV") == "test":
    DATABASE_URL = "sqlite:///./test_db.sqlite"
else:
    DATABASE_URL = "sqlite:///./produit_api.db"

# Créez une session de base de données
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialisez la base de données pour les tests
@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    yield db
    db.close()

@given('je crée un produit avec le nom "{name}","{details}" et la quantité {quantity:d}')
async def create_product(context, name, details, quantity):
    produit_data = {"name": name, "details": details, "stock": quantity}
    context.produit_created = await create_produit(produit_data, db())

@then('je récupère tous les produits')
async def get_all_products(context):
    context.produits = await read_produits(db)

@when('je supprime le produit avec l\'ID {product_id:d}')
async def delete_product(context, product_id):
    await delete_produit(product_id, db)

@then('le produit est créé')
def check_product_created(context):
    assert read_produits().__sizeof__() > 0

@then('je reçois une liste de produits')
async def check_products_received(context):
    response = await read_produits(db)
    assert response == context.produits

@then('le produit est supprimé avec succès')
async def check_product_deleted(context):
    assert await delete_produit(context.produits[0].id, db) is not None

@then('je reçois le produit spécifique avec l\'ID {product_id:d}')
async def check_specific_product_received(context, product_id):
    assert await read_specific_produit(product_id, db()) == context.produits[0]

@then('un message RabbitMQ est envoyé avec les détails du produit {name} {quantity}')
@patch('api.produit_api.connect_rabbitmq')
async def check_rabbitmq_message_sent(mock_connect_rabbitmq, name, quantity):
    mock_channel = mock_connect_rabbitmq.return_value
    mock_channel.basic_get.return_value = (None, None, f"Produit créé: {name} avec quantité: {quantity}".encode('utf-8'))

    produit_data = {"name": name, "details": "{}", "stock": quantity}
    await create_produit(produit_data, db)

    mock_connect_rabbitmq.assert_called_once()
    mock_channel.basic_publish.assert_called_once_with(exchange='', routing_key='produit_queue', body=f"Produit créé: {name} avec quantité: {quantity}")
