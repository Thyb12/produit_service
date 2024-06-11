# Utiliser une image de Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis dans le conteneur
COPY requirements.txt .
COPY api/produit_api.py /app/produit_api.py
COPY tests /app/tests

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application FastAPI écoute
EXPOSE 8888

# Définir la commande à exécuter lorsque le conteneur démarre
CMD ["uvicorn", "produit_api:app", "--host", "0.0.0.0", "--port", "8888"]
