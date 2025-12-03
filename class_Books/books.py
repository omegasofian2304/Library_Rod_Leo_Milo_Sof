from sqlalchemy import Column, Integer, String, Date, Boolean
from db.database import Base

class Book(Base):
    __tablename__ = 'books'

    # Attributs privés (_)
    _id = Column("id", Integer, primary_key=True)
    _title = Column("title", String)
    _nb_pages = Column("nb_pages", Integer)
    _genre = Column("genre", String)
    _summary = Column("summary", String)
    _format = Column("format", String)
    _release_date = Column("release_date", Date)
    _image = Column("Image", String)
    _status = Column("status", Boolean)

    # Constructeur
    def __init__(self, title, nb_pages, genre, summary, format_, release_date, image, status):
        self._title = title
        self._nb_pages = nb_pages
        self._genre = genre
        self._summary = summary
        self._format = format_
        self._release_date = release_date
        self._image = image
        self._status = status

    # Propriétés pour accéder aux attributs privés

    #getter
    @property
    def id(self):
        return self._id
    @property
    def title(self):
        return self._title
    #setter
    @title.setter
    def title(self, value):
        self._title = value

    @property
    def nb_pages(self):
        return self._nb_pages

    @nb_pages.setter
    def nb_pages(self, value):
        self._nb_pages = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, value):
        self._release_date = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
