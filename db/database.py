"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : création du fichier de base qui accueillera la session, le moteur et la classe "Base".
"""
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


# Création de la classe qui sera la base pour tous les autres modèles
class Base(DeclarativeBase):
    pass


# Créer le moteur sqlite
DATABASE_URL = "sqlite:///./mydatabase.db"

# echo=True pour afficher les logs dans la console
engine = create_engine(DATABASE_URL, echo=True)

# Création de session
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()
