"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : création du fichier de la classe "person".
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date
from db.database import Base


class Person(Base):
    __abstract__ = True

    # liste des attributs
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    birthDate: Mapped[Date] = mapped_column(Date, nullable=False)