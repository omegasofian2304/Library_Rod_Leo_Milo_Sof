"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : Fichier de base pour SQLAlchemy : engine, session et initialisation
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
from Classes.base import Base


# Création du moteur SQLite (echo=False pour ne pas afficher le SQL)
DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(DATABASE_URL, echo=False)

# Création des sessions
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


def init_database():
    """
    Crée toutes les tables et ajoute des données de test
    """
    # Importer les modèles avant création des tables
    from Classes.person import Person
    from Classes.employee import Employee
    from Classes.author import Author
    from Classes.customer import Customer
    from Classes.books import Book
    from Classes.borrow import Borrow
    from Classes.publisher import Publisher

    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)

    session = get_session()

    try:
        # Employé admin
        if not session.query(Employee).filter_by(_isAdmin=True).first():
            admin = Employee(
                firstname="Admin",
                lastname="Bibliothèque",
                birthdate=date(1980, 1, 1),
                _email="admin@bibliotheque.ch",
                _monthlySalary=5000.0,
                _arrivalDate=date(2020, 1, 1),
                _workPercentage=100,
                _isAdmin=True,
                _password="Pa$$w0rd"
            )
            session.add(admin)
            session.commit()

        # Auteur
        if not session.query(Author).filter_by(_nickName="Edmond Rostand").first():
            admin.addAuthor(
                session=session,
                firstName="Edmond",
                lastName="Rostand",
                birthDate=date(1868, 4, 1),
                nickname="Edmond Rostand"
            )

        # Éditeur
        if not session.query(Publisher).filter_by(_name="Fasquelle").first():
            admin.addPublisher(
                session=session,
                name="Fasquelle",
                location="Paris, France",
                creationDate=date(1897, 1, 1)
            )

        # Livre
        if not session.query(Book).filter_by(_title="Cyrano de Bergerac").first():
            author = session.query(Author).filter_by(_nickName="Edmond Rostand").first()
            publisher = session.query(Publisher).filter_by(_name="Fasquelle").first()
            admin.addBook(
                session=session,
                title="Cyrano de Bergerac",
                nbPages=232,
                genre="Théâtre",
                summary="Comédie héroïque en cinq actes et en vers d'Edmond Rostand. L'histoire d'un poète et soldat au grand nez qui aime en secret sa cousine Roxane.",
                format="livre de poche",
                releaseDate=date(1897, 12, 28),
                image="https://cdn1.booknode.com/book_cover/10/full/cyrano-de-bergerac-10146.jpg",
                authorId=author._id,
                publisherId=publisher._id
            )

        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_database()
