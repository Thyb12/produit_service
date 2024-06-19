# API FastAPI pour la gestion des produits

## Table des matières

- [Description](#description)
- [Schéma d'architecture](#schéma-darchitecture)
- [Sécurité de l’API](#sécurité-de-lapi)
- [Langage de programmation](#langage-de-programmation)
- [Règles d’hébergement](#règles-dhébergement)
- [Gestion du code source](#gestion-du-code-source)
- [Gestion du déploiement](#gestion-du-déploiement)
- [Utilisation](#utilisation)

## Description

Cette API est construite avec FastAPI pour gérer des produits. Elle utilise SQLAlchemy pour la gestion de la base de données, Prometheus pour les métriques, et RabbitMQ pour la messagerie asynchrone. L'API fournit des endpoints pour créer, lire et supprimer des produits.

## Schéma de l'architecture de l'application

L'application est composée de plusieurs composants :

1. **FastAPI** : Application principale servant les endpoints de l'API.
2. **SQLAlchemy** : ORM utilisé pour interagir avec la base de données SQLite.
3. **RabbitMQ** : Utilisé pour la messagerie asynchrone entre le producteur et le consommateur.
4. **Prometheus** : Utilisé pour surveiller les métriques de l'API.

L'architecture de l'application se présente comme suit :

```plaintext
+-------------------------+      +-------------------------+
|                         |      |                         |
|     Client HTTP         |      |      Prometheus         |
|  (Postman, Browser)     |      |                         |
+-----------+-------------+      +-----------+-------------+
            |                                |
            |                                |
            v                                v
+-----------+-------------+      +-----------+-------------+
|                         |      |                         |
|        FastAPI          +------>     /metrics endpoint   |
|                         |      |                         |
|                         |      |                         |
+-----------+-------------+      +-------------------------+
            |
            |
            v
+-----------+-------------+
|                         |
|        SQLite           |
|                         |
+-------------------------+
            |
            v
+-------------------------+
|                         |
|       RabbitMQ          |
|                         |
+-------------------------+
            |
            |
            v
+-----------+-------------+
|                         |
|      Producteur         |
|                         |
+-----------+-------------+
            |
            v
+-----------+-------------+
|                         |
|       Consommateur      |
|                         |
+-------------------------+
```

## Sécurité de l’API

Pour garantir la sécurité de l'API, plusieurs mesures ont été mises en place :

- **Limitation des taux** : Limite le nombre de tentatives de connexion pour éviter les abus.
- **Validation des données** : Utilisation de Pydantic pour valider les entrées utilisateur, ce qui aide à prévenir les attaques par injection.
- **Gestion des erreurs** : Utilisation d'HTTPException pour gérer les erreurs et fournir des messages d'erreur appropriés.

## Langage de programmation

L'API est développée en Python avec le framework FastAPI. Les bibliothèques principales utilisées sont :

- **FastAPI** : Framework web pour construire l'API.
- **SQLAlchemy** : ORM pour interagir avec la base de données.
- **Pydantic** : Pour la validation des données.
- **Prometheus-client** : Pour l'intégration des métriques Prometheus.
- **Pika** : Pour la communication avec RabbitMQ.

## Règles d’hébergement

Pour l'hébergement de l'API, il est recommandé d'utiliser des conteneurs Docker pour une portabilité et une scalabilité optimales. Voici quelques bonnes pratiques :

- **Utilisation de Docker** : Conteneuriser l'application pour faciliter le déploiement et la scalabilité.
- **Hébergement cloud** : Utiliser des services comme AWS, Google Cloud Platform, ou Azure pour héberger l'application.
- **Scalabilité horizontale** : Ajouter plus d'instances de l'API et utiliser un load balancer pour répartir les requêtes.

## Utilisation

### Lancer l'API

1. Cloner le dépôt :

   ```bash
   git clone <repository_url>
   cd produit_api
    ```
2. Construire et lancer les conteneurs avec Docker Compose

   ```bash
   docker-compose up --build
   ```
   L'API sera disponible sur http://localhost:8888.

## Endpoints principaux

- **Créer un produit** : `POST /produits/create`
- **Lire tous les produits** : `GET /produits/all`
- **Lire un produit spécifique** : `GET /produit/{produit_id}`
- **Supprimer un produit** : `DELETE /produits/{produit_id}`
- **Métriques Prometheus** : `GET /metrics`

## Exemples de requêtes

### Créer un produit

   ```bash
   curl -X POST "http://localhost:8888/produits/create" -H "Content-Type: application/json" -d '{"name": "Produit1", "details": "{}", "stock": 10}'
   ```

### Lire tous les produits

   ```bash
    curl -X GET "http://localhost:8888/produits/all"
   ```
### Lire un produit spécifique

   ```bash
    curl -X GET "http://localhost:8888/produit/1"
   ```

### Supprimer un produit

   ```bash
    curl -X DELETE "http://localhost:8888/produits/1"
   ```