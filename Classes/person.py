"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : création du fichier de la classe "person".
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from Classes.base import Base


class Person(Base):
    __abstract__ = True

    # liste des attributs communs à toutes les personnes
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[Date] = mapped_column(Date, nullable=False)