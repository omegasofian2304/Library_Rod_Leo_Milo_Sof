"""
Auteur : Rodrigo Silva Riço
Date : 17.12.2025
Projet : Création du fichier qui contiendra la classe Customer
"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Classes.person import Person


class Customer(Person):
    __tablename__ = 'customer'

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _email: Mapped[str] = mapped_column(String(50), nullable=False)
    _fine: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # relation bidirectionnelle avec Borrow
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="customer")