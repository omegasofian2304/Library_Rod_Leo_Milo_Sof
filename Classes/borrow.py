"""
Auteur : Rodrigo Silva Riço et Sofian Hussein
Date : 17.13.2025
Projet : Création du fichier qui contiendra la classe borrow
"""

from sqlalchemy import Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from publisher import Publisher
from books import Book
from customer import Customer

from db.database import Base


class Borrow(Base):
    __tablename__ = 'borrow'
    ''' 
    Remarque : En Python, les attributs précédés d'un underscore (_) ne sont pas réellement privés.
    C'est juste une convention pour indiquer qu'ils sont destinés à un usage interne.
    Il est toujours possible d'y accéder depuis l'extérieur de la classe (ex: instance._id).
    '''

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _borrowDate: Mapped[Date] = mapped_column(Date, nullable=False)
    _returnDate: Mapped[Date] = mapped_column(Date, nullable=False)
    _returned: Mapped[Boolean] = mapped_column(Boolean, nullable=False)

    # création des relations
    book_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    book: Mapped["book"] = relationship("Customer")

    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["customer"] = relationship("Customer")
