"""
Auteur : Rodrigo Silva Riço
Date : 03.13.2025
Projet : Création du fichier qui contiendra la classe Books
"""
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from publisher import Publisher

from db.database import Base


class Book(Base):

    ''' 
    Remarque : En Python, les attributs précédés d'un underscore (_) ne sont pas réellement privés.
    C'est juste une convention pour indiquer qu'ils sont destinés à un usage interne.
    Il est toujours possible d'y accéder depuis l'extérieur de la classe (ex: instance._id).
    '''

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _title: Mapped[str] = mapped_column(String(200), nullable=False)
    _nb_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    _genre: Mapped[str] = mapped_column(String(25), nullable=False)
    _summary: Mapped[str] = mapped_column(String(200), nullable=False)
    _format: Mapped[str] = mapped_column(String(15), nullable=False)
    _release_date: Mapped[Date] = mapped_column(Date, nullable=False)
    _image: Mapped[str] = mapped_column(String(200), nullable=False)
    _status: Mapped[str] = mapped_column(String(25), nullable=False)

    # création
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    publisher: Mapped["Publisher"] = relationship("publisher")
