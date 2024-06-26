Feature: Gestion des produits dans l'API

  Scenario: Créer un nouveau produit
    Given je crée un produit avec le nom "1Produit" "test" et la quantité 1
    Then le produit est créé

  Scenario: Récupérer tous les produits
    Given je crée un produit avec le nom "2Produit" "test" et la quantité 1
    And je crée un produit avec le nom "2.1Produit" "test" et la quantité 2
    And je crée un produit avec le nom "2.3Produit" "test" et la quantité 3
    Then je reçois une liste de produits

  Scenario: Supprimer un produit existant
    Given je crée un produit avec le nom "3Produit" "test" et la quantité 666
    When je supprime le produit avec l'ID 1
    Then le produit est supprimé avec succès

  Scenario: Récupérer un produit spécifique par son ID
    Given je crée un produit avec le nom "4Produit" "test" et la quantité 123
    Then je reçois le produit spécifique avec l'ID 1

  Scenario: Vérifier l'envoi d'un message RabbitMQ lors de la création d'un produit
    Given je crée un produit avec le nom "5Produit" "test" et la quantité 42
    Then un message RabbitMQ est envoyé avec les détails du produit "5Produit" 10
