"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : création du fichier de la classe "person".
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date
from db.database import Base


# création de la classe abstraite Person
class Person(Base):
    __abstract__ = True  # nous déclarons la classe comme abstraite

    # liste des attributs
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[Date] = mapped_column(Date, nullable=False)
