from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Création de l'instance FastAPI pour initialiser l'application et permettre la définition des routes.
app = FastAPI()

# Configuration et mise en place de la connexion à la base de données avec sqlalchemy
DATABASE_URL = "sqlite:///./produit_api.db"
DATABASE_URL_TEST = "sqlite:///./test_db.sqlite"

def get_engine(env: str = "prod"):
    if env == "test":
        return create_engine(DATABASE_URL_TEST)
    else:
        return create_engine(DATABASE_URL)

# Définition d'une fonction pour obtenir une session de base de données en fonction de l'environnement
def get_db(env: str = "prod"):
    engine = get_engine(env)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Définition d'un modèle de données pour un produit dans la base de données
Base = declarative_base()

class Produit(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)

# Création d'un modèle pydantic pour la création de produit
class ProduitCreate(BaseModel):
    name: str
    quantity: int

# Création d'un modèle pydantic pour la réponse de produit
class ProduitResponse(ProduitCreate):
    id: int

    class Config:
        orm_mode = True

# Route POST pour créer un nouveau produit dans l'API
@app.post("/produits/create", response_model=ProduitResponse)
async def create_produit(produit: ProduitCreate, db: Session = Depends(get_db)):
    db_produit = Produit(name=produit.name, quantity=produit.quantity)
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit

# Route GET pour voir tous les produits
@app.get("/produits/all", response_model=List[ProduitResponse])
async def read_produits(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    produits = db.query(Produit).offset(skip).limit(limit).all()
    return produits

# Route DELETE pour supprimer un produit par son id
@app.delete("/produits/{produit_id}")
async def delete_produit(produit_id: int, db: Session = Depends(get_db)):
    db_produit = db.query(Produit).filter(Produit.id == produit_id).first()
    if db_produit is None:
        raise HTTPException(status_code=404, detail="Produit not found")
    db.delete(db_produit)
    db.commit()
    return {"detail": "Produit deleted"}

# Route GET pour voir un produit spécifique par son id
@app.get("/produit/{produit_id}", response_model=ProduitResponse)
async def read_specific_produit(produit_id: int, db: Session = Depends(get_db)):
    db_produit = db.query(Produit).filter(Produit.id == produit_id).first()
    if db_produit is None:
        raise HTTPException(status_code=404, detail="Produit not found")
    return db_produit
