"""
Auteur : Rodrigo Silva Riço
Date : 17.12.2025
Projet : Création du fichier qui contiendra la classe Author
"""
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Classes.person import Person
from Classes.base import Base


class Author(Person):
    __tablename__ = 'author'

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _nickName: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relation inverse avec Book
    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")