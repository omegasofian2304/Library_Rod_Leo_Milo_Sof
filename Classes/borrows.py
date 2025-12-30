"""
Auteur : Sofian Hussein
Date : 30.12.2025
Projet : création du fichier de la classe "borrows".
"""
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class Borrows(Base):
    __tablename__ = 'borrows'
    ''' 
    Remarque : En Python, les attributs précédés d'un underscore (_) ne sont pas réellement privés.
    C'est juste une convention pour indiquer qu'ils sont destinés à un usage interne.
    Il est toujours possible d'y accéder depuis l'extérieur de la classe (ex: instance._id).
    '''

    # liste des attributs
    _borrowDate: Mapped[Date] = mapped_column(Integer, primary_key=True)
    _returnDate: Mapped[Date] = mapped_column(String, primary_key=True)
    _dueDate: Mapped[Date] = mapped_column(String, primary_key=True)
    _returned: Mapped[bool] = mapped_column(Integer, primary_key=True)