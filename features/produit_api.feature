Feature: Gestion des produits dans l'API

  Scenario: Créer un nouveau produit
    Given je crée un produit avec le nom "Nouveau produit" et la quantité 10
    Then le produit est créé avec l'ID associé

  Scenario: Récupérer tous les produits
    When je récupère tous les produits
    Then je reçois une liste de produits

  Scenario: Supprimer un produit existant
    Given un produit avec l'ID 1 existe
    When je supprime le produit avec l'ID 1
    Then le produit est supprimé avec succès

  Scenario: Récupérer un produit spécifique par son ID
    Given un produit avec l'ID 1 existe
    When je récupère le produit avec l'ID 1
    Then je reçois le produit spécifique avec l'ID 1
