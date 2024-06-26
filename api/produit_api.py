import os
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from prometheus_client import Summary, Counter, generate_latest, CONTENT_TYPE_LATEST
import logging
import pika
from datetime import datetime, timedelta

logger = logging.getLogger("uvicorn.error")

# Création de l'instance FastAPI pour initialiser l'application et permettre la définition des routes.
app = FastAPI()

# Configuration et mise en place de la connexion à la base de données avec MongoDB
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "MSPR_1"
COLLECTION_NAME = "produits"
RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE = "produit_queue"
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Création d'un modèle pydantic pour la création de produit
class ProduitCreate(BaseModel):
    name: str
    details: str
    stock: int

# Création d'un modèle pydantic pour la réponse de produit
class ProduitResponse(ProduitCreate):
    id: str
    createdAt: Optional[datetime]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

# Définir des métriques Prometheus
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Total count of requests')


# Middleware pour mesurer le temps de traitement des requêtes
@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    with REQUEST_TIME.time():
        response = await call_next(request)
        REQUEST_COUNT.inc()
    return response

# Route pour exposer les métriques
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def connect_rabbitmq():
    try:
        parameters = pika.ConnectionParameters(RABBITMQ_HOST)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        return channel
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise HTTPException(status_code=500, detail="Could not connect to RabbitMQ")

failed_attempts = {}

# Fonction pour vérifier et limiter les tentatives de connexion
def rate_limiting(ip_address: str):
    now = datetime.now()
    if ip_address in failed_attempts:
        attempt_info = failed_attempts[ip_address]
        last_attempt_time = attempt_info["timestamp"]
        attempts = attempt_info["count"]
        logger.info(f"IP {ip_address}: {attempts} attempts, last attempt at {last_attempt_time}")
        # Si moins de 60 secondes depuis la dernière tentative, augmenter le compteur de tentatives
        if now - last_attempt_time < timedelta(seconds=60):
            attempts += 1
            failed_attempts[ip_address] = {"count": attempts, "timestamp": now}
            # Si plus de 5 tentatives dans les 60 secondes, déclencher la limitation
            if attempts > 5:
                raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
        else:
            # Réinitialiser après 60 secondes
            failed_attempts[ip_address] = {"count": 1, "timestamp": now}
    else:
        failed_attempts[ip_address] = {"count": 1, "timestamp": now}
    logger.info(f"IP {ip_address}: allowed")

# Route POST pour créer un nouveau produit dans l'API
@app.post("/produits/create", response_model=ProduitResponse)
async def create_produit(produit: ProduitCreate, request: Request):
    client_ip = request.client.host
    rate_limiting(client_ip)  # Limiter les tentatives de connexion par adresse IP

    produit_data = produit.dict()
    produit_data["createdAt"] = datetime.utcnow()
    result = collection.insert_one(produit_data)
    produit_data["id"] = str(result.inserted_id)

    try:
        # Envoyer un message à RabbitMQ
        channel = connect_rabbitmq()
        message = f"Produit créé: {produit.name} avec détails: {produit.details} et stock: {produit.stock}"
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
        channel.close()
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message RabbitMQ : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

    return produit_data

# Route GET pour voir tous les produits
@app.get("/produits/all", response_model=List[ProduitResponse])
async def read_produits(skip: int = 0, limit: int = 10):
    produits = list(collection.find().skip(skip).limit(limit))
    for produit in produits:
        produit["id"] = str(produit["_id"])
        del produit["_id"]
    return produits

# Route DELETE pour supprimer un produit par son id
@app.delete("/produits/{produit_id}")
async def delete_produit(request: Request, produit_id: str):
    client_ip = request.client.host
    rate_limiting(client_ip)  # Limiter les tentatives de connexion par adresse IP

    result = collection.delete_one({"_id": ObjectId(produit_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Produit not found")
    return {"detail": "Produit deleted"}

# Route GET pour voir un produit spécifique par son id
@app.get("/produit/{produit_id}", response_model=ProduitResponse)
async def read_specific_produit(produit_id: str):
    produit = collection.find_one({"_id": ObjectId(produit_id)})
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit not found")
    produit["id"] = str(produit["_id"])
    del produit["_id"]
    return produit

# Route PUT pour mettre à jour un produit par son id
@app.put("/produits/{produit_id}", response_model=ProduitResponse)
async def update_produit(produit_id: str, produit: ProduitCreate, request: Request):
    client_ip = request.client.host
    rate_limiting(client_ip)  # Limiter les tentatives de connexion par adresse IP

    update_data = produit.dict()
    result = collection.update_one({"_id": ObjectId(produit_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Produit not found")

    produit = collection.find_one({"_id": ObjectId(produit_id)})
    produit["id"] = str(produit["_id"])
    del produit["_id"]
    return produit
