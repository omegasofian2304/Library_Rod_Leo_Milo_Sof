"""
Auteur : Rodrigo Silva Riço
Date : 03.13.2025
Projet : Création du fichier qui contiendra la classe Books
"""
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, MappedColumn

from db.database import Base

class Books(Base):
    __tablename__ = 'Books'

    # Attributs privés
    _id: Mapped[int] = MappedColumn(Integer, primary_key=True)
    _title: Mapped[str] = MappedColumn(String(200), nullable=False)
    _nb_pages: Mapped[int] = MappedColumn(Integer, nullable=False)
    _genre: Mapped[str] = MappedColumn(String(25), nullable=False)
    _summary: Mapped[str] = MappedColumn(String(200), nullable=False)
    _format: Mapped[str] = MappedColumn(String(15), nullable=False)
    _release_date: Mapped[Date] = MappedColumn(Date, nullable=False)
    _image: Mapped[str] = MappedColumn(String(200), nullable=False)
    _status: Mapped[str] = MappedColumn(String(25), nullable=False)
