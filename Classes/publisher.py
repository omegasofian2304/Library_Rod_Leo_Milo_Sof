"""
Auteur : Sofian Hussein
Date : 10.12.2025
Projet : création du fichier de la classe "publisher".
"""
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from Classes.base import Base


class Publisher(Base):
    __tablename__ = 'publisher'

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _name: Mapped[str] = mapped_column(String(100), nullable=False)
    _location: Mapped[str] = mapped_column(String(100), nullable=False)
    _creation_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # relation bidirectionnelle avec Book
    books: Mapped[list["Book"]] = relationship("Book", back_populates="publisher")