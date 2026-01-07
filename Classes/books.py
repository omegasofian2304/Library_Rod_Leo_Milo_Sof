"""
Auteur : Rodrigo Silva Riço
Date : 03.13.2025
Projet : Création du fichier qui contiendra la classe Books
"""
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.database import Base


class Book(Base):
    __tablename__ = 'book'

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _title: Mapped[str] = mapped_column(String(200), nullable=False)
    _nb_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    _genre: Mapped[str] = mapped_column(String(25), nullable=False)
    _summary: Mapped[str] = mapped_column(String(200), nullable=False)
    _format: Mapped[str] = mapped_column(String(15), nullable=False)
    _release_date: Mapped[Date] = mapped_column(Date, nullable=False)
    _image: Mapped[str] = mapped_column(String(200), nullable=False)
    _status: Mapped[str] = mapped_column(String(25), nullable=False, default="available")

    # foreign keys
    author_id: Mapped[int] = mapped_column(ForeignKey("author._id"), nullable=False)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher._id"), nullable=False)

    # relations bidirectionnelles
    author: Mapped["Author"] = relationship("Author", back_populates="books")
    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="book")