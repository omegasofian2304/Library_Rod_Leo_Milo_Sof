"""
Auteur : Rodrigo Silva Riço et Sofian Hussein
Date : 17.13.2025
Projet : Création du fichier qui contiendra la classe borrow
"""
from sqlalchemy import Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from Classes.base import Base


class Borrow(Base):
    __tablename__ = 'borrow'

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _returnDate: Mapped[Date] = mapped_column(Date, nullable=True)
    _borrowDate: Mapped[Date] = mapped_column(Date, nullable=False)
    _dueDate: Mapped[Date] = mapped_column(Date, nullable=False)
    _returned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # foreign keys
    book_id: Mapped[int] = mapped_column(ForeignKey("book._id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer._id"), nullable=False)

    # relations bidirectionnelles
    book: Mapped["Book"] = relationship("Book", back_populates="borrows")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="borrows")