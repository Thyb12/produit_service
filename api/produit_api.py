from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Création de l'instance FastAPI pour initialiser l'application et permettre la définition des routes.
app = FastAPI()

#Configuration et mise en place de la connexion à la base de données avec sqlalchemy
DATABASE_URL = "sqlite:///./produit_api.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Définition d'un modèle de données pour un produit dans la base de données
class Produit(Base) :
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)

Base.metadata.create_all(bind=engine)

#Création d'un modèle pydantic (bibliothèque fournissant des fonctionnalités de validation des données et de conversion de type)
class ProduitCreate(BaseModel) :
    
    name: str
    quantity: int


#Création d'un modèle pydantic (bibiothèque fournissant des foncitonnalités de validation des données et de conversion de type)
class ProduitResponse(ProduitCreate) :

    id: int

    class Config :
        orm_mode = True


#Route POST pour créer un nouveau produit dans l'API
@app.post("/produits/create", response_model=ProduitResponse)
async def create_produit(produit: ProduitCreate):
    db = SessionLocal()
    db_produit = Produit(name=produit.name, quantity=produit.quantity)
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    db.close()
    return db_produit



#Route GET pour voir tous les produits
@app.get("/produits/all", response_model=List[ProduitResponse])
async def read_produits(skip: int = 0, limit: int = 10) :
    db = SessionLocal()
    produits = db.query(Produit).offset(skip).limit(limit).all()
    db.close()
    return produits


#Route DELETE pour supprimer un produit par son id
@app.delete("/produits/{produit_id}")
async def delete_produit(produit_id: int) :
    db = SessionLocal()
    db_produit = db.query(Produit).filter(Produit.id == produit_id).first()
    if db_produit is None :
        db.close()
        raise HTTPException(status_code=404, detail="Produit not found")
    db.delete(db_produit)
    db.commit()
    db.close()
    return {"detail" : "Produit deleted"}


#Route GET pour voir un produit spécifique par son id
@app.get("/produit/{produit_id}")
async def read_specific_produit(produit_id: int) :
    db = SessionLocal()
    db_produit = db.query(Produit).filter(Produit.id == produit_id).first()
    if db_produit is None :
        db.close()
        raise HTTPException(status_code=404, detail="Produit not found")
    db.close()
    return db_produit