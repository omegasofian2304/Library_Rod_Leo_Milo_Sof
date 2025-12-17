"""
Auteur : Sofian Hussein
Date : 10.12.2025
Projet : création du fichier de la classe "publisher".
"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class Publisher(Base):
    __tablename__ = 'publisher'
    ''' 
    Remarque : En Python, les attributs précédés d'un underscore (_) ne sont pas réellement privés.
    C'est juste une convention pour indiquer qu'ils sont destinés à un usage interne.
    Il est toujours possible d'y accéder depuis l'extérieur de la classe (ex: instance._id).
    '''

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _name: Mapped[str] = mapped_column(String, primary_key=True)
    _location: Mapped[str] = mapped_column(String, primary_key=True)
    _creation_date: Mapped[int] = mapped_column(Integer, primary_key=True)