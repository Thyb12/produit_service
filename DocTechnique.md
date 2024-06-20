# Documentation Technique

## Langage de programmation

### Python avec FastAPI

L'API est développée en Python, un langage de programmation interprété, orienté objet et de haut niveau, avec une sémantique dynamique. Python est reconnu pour sa lisibilité et sa simplicité, ce qui accélère le développement tout en réduisant les coûts de maintenance.

#### Pourquoi Python ?

1. **Lisibilité et Simplicité** : Python est connu pour sa syntaxe claire et concise, facilitant ainsi la lecture et l'écriture du code.
2. **Richesse de l'écosystème** : Python possède une vaste bibliothèque standard et une multitude de bibliothèques tierces pour pratiquement toutes les applications, de la science des données au développement web.
3. **Communauté Active** : Une communauté large et active qui contribue à l'amélioration continue du langage et à la disponibilité de nombreuses ressources d'apprentissage.

### FastAPI

FastAPI est un framework web moderne, rapide (haute performance), conçu pour la création d'APIs avec Python 3.6+ basé sur les annotations de type Python.

#### Pourquoi FastAPI ?

1. **Performance** : FastAPI est l'un des frameworks web Python les plus rapides grâce à son utilisation d'ASGI (Asynchronous Server Gateway Interface) et de la bibliothèque Starlette.
2. **Facilité d'utilisation** : FastAPI simplifie le développement d'API en offrant des fonctionnalités intégrées pour la validation des données, la génération automatique de documentation (OpenAPI et JSON Schema), et la gestion des requêtes et des réponses.
3. **Type Safety** : Utilisation des annotations de type Python pour une vérification des types à la compilation, réduisant ainsi les erreurs de runtime.

### Bibliothèques utilisées

- **SQLAlchemy** : ORM (Object-Relational Mapping) pour interagir avec la base de données de manière déclarative.
- **Pydantic** : Pour la validation des données via des modèles de données robustes.
- **Prometheus-client** : Pour l'intégration des métriques Prometheus.
- **Pika** : Pour la communication avec RabbitMQ.

## Gestion du code source

### Git et GitHub

Le code source de l'API est géré en utilisant Git, un système de contrôle de version distribué, et est hébergé sur GitHub, une plateforme de développement collaboratif.

#### Pourquoi Git ?

1. **Contrôle de version** : Git permet de suivre les modifications du code, de gérer différentes versions et de collaborer efficacement avec d'autres développeurs.
2. **Branches** : Facilite le développement de nouvelles fonctionnalités ou la correction de bugs sans affecter le code principal (branche `main`).
3. **Historique des modifications** : Permet de revenir à un état antérieur du projet si nécessaire, avec un historique détaillé des changements et des commits.

#### Structure du dépôt Git

- **Branche `main`** : Contient le code stable et prêt pour la production.
- **Branches `feature/*`** : Utilisées pour le développement de nouvelles fonctionnalités.
- **Branches `bugfix/*`** : Utilisées pour les corrections de bugs.

### Intégration Continue / Déploiement Continu (CI/CD)

Le pipeline CI/CD est configuré avec GitHub Actions pour automatiser les processus de build, de test et de déploiement.

#### Configuration du pipeline CI/CD

Le fichier `.github/workflows/ci-pipeline.yml` configure le pipeline CI/CD :

- **Build et Analyse** : Installe les dépendances, exécute les tests avec couverture de code, et effectue une analyse statique du code avec SonarQube.
- **Tests** : Utilise `coverage` pour mesurer la couverture de code et `behave` pour exécuter les tests de comportement.
- **Scan de Sécurité** : Intègre SonarQube pour analyser le code source à la recherche de vulnérabilités et de mauvaises pratiques.

Ce pipeline garantit que le code est constamment testé et analysé avant d'être fusionné dans la branche principale, améliorant ainsi la qualité et la sécurité du code.