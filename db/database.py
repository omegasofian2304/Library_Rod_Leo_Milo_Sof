"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : création du fichier de base qui accueillera la session, le moteur et la classe "Base".
"""
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from datetime import date


# Création de la classe qui sera la base pour tous les autres modèles
class Base(DeclarativeBase):
    pass


# Créer le moteur sqlite
DATABASE_URL = "sqlite:///./mydatabase.db"

# echo=True pour afficher les logs dans la console
engine = create_engine(DATABASE_URL, echo=True)

# Création de session
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


# Fonction pour initialiser la base de données avec des données de test
def init_database():
    """Crée les tables et ajoute des données initiales"""
    from Classes.employee import Employee
    from Classes.author import Author
    from Classes.publisher import Publisher
    from Classes.books import Book

    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)

    session = get_session()

    try:
        # Vérifier si un employé admin existe déjà
        existing_employee = session.query(Employee).filter_by(_isAdmin=True).first()

        if not existing_employee:
            # Créer un employé admin
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
            print("Employé admin créé")
        else:
            admin = existing_employee
            print("Employé admin existant trouvé")

        # Vérifier si l'auteur existe déjà
        existing_author = session.query(Author).filter_by(_nickName="Edmond Rostand").first()

        if not existing_author:
            # Créer l'auteur Edmond Rostand
            author = admin.addAuthor(
                session=session,
                firstName="Edmond",
                lastName="Rostand",
                birthDate=date(1868, 4, 1),
                nickname="Edmond Rostand"
            )
            print("Auteur Edmond Rostand créé ✓")
        else:
            author = existing_author
            print("Auteur existant trouvé ✓")

        # Vérifier si l'éditeur existe déjà
        existing_publisher = session.query(Publisher).filter_by(_name="Fasquelle").first()

        if not existing_publisher:
            # Créer l'éditeur
            publisher = admin.addPublisher(
                session=session,
                name="Fasquelle",
                location="Paris, France",
                creationDate=date(1897, 1, 1)
            )
            print("Éditeur Fasquelle créé ✓")
        else:
            publisher = existing_publisher
            print("Éditeur existant trouvé ✓")

        # Vérifier si le livre existe déjà
        existing_book = session.query(Book).filter_by(_title="Cyrano de Bergerac").first()

        if not existing_book:
            # Ajouter le livre Cyrano de Bergerac
            book = admin.addBook(
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
            print("Livre 'Cyrano de Bergerac' ajouté")
        else:
            print("Livre 'Cyrano de Bergerac' existe déjà")

        print("Base de données initialisée avec succès !")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'initialisation : {e}")
    finally:
        session.close()


# Appeler cette fonction pour initialiser la base
if __name__ == "__main__":
    init_database()