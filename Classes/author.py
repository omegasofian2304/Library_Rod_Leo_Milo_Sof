"""
Auteur : Rodrigo Silva Riço
Date : 17.12.2025
Projet : Création du fichier qui contiendra la classe Author
"""
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, MappedColumn
from person import Person


class Author(Person):
    __tablename__ = 'author'
    ''' 
    Remarque : En Python, les attributs précédés d'un underscore (_) ne sont pas réellement privés.
    C'est juste une convention pour indiquer qu'ils sont destinés à un usage interne.
    Il est toujours possible d'y accéder depuis l'extérieur de la classe (ex: instance._id).
    '''

    #liste des attributs
    _id: Mapped[int] = MappedColumn(Integer, primary_key=True)
    _nickName: Mapped[str] = MappedColumn(String(50), nullable=False)
