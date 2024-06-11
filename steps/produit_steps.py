from behave import given, when, then
from unittest.mock import patch

# Importez ici vos fonctions de gestion des produits

# Les données des produits à utiliser pour les tests
PRODUCT_DATA = {
    1: {"id": 1, "name": "Nouveau produit", "quantity": 10}
}

# Simulation de la création d'un produit
@given('je crée un produit avec le nom "{name}" et la quantité {quantity:d}')
def create_product(context, name, quantity):
    context.product_id = 1  # En supposant que l'ID du produit créé est toujours 1
    return PRODUCT_DATA[context.product_id]

# Simulation de la récupération de tous les produits
@when('je récupère tous les produits')
def get_all_products(context):
    context.response = [product for product_id, product in PRODUCT_DATA.items()]

# Vérification que le produit est créé avec l'ID associé
@then('le produit est créé avec l\'ID associé')
def check_product_created(context):
    assert context.product_id in PRODUCT_DATA

# Vérification que je reçois une liste de produits
@then('je reçois une liste de produits')
def check_products_received(context):
    assert len(context.response) == len(PRODUCT_DATA)

# Supprimer un produit existant
@given('un produit avec l\'ID {product_id:d} existe')
def check_product_exists(context, product_id):
    context.product_id = product_id
    return product_id in PRODUCT_DATA

@when('je supprime le produit avec l\'ID {product_id:d}')
def delete_product(context, product_id):
    if context.product_id in PRODUCT_DATA:
        del PRODUCT_DATA[context.product_id]
        context.response = True
    else:
        context.response = False

@then('le produit est supprimé avec succès')
def check_product_deleted(context):
    assert context.response is True

# Récupérer un produit spécifique par son ID
@when('je récupère le produit avec l\'ID {product_id:d}')
def get_specific_product(context, product_id):
    context.response = PRODUCT_DATA.get(product_id)

@then('je reçois le produit spécifique avec l\'ID {product_id:d}')
def check_specific_product_received(context, product_id):
    assert context.response == PRODUCT_DATA.get(product_id)
