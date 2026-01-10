"""
Auteur : Sofian Hussein
Date : 03.12.2025
Projet : Fichier de base pour SQLAlchemy : engine, session et initialisation
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
from Classes.base import Base
import os

# IMPORTANT : Chemin absolu vers le dossier db/
# Cela garantit que la DB sera toujours créée dans db/ peu importe d'où on lance le script
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "mydatabase.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"📂 Base de données configurée : {DB_PATH}")

# Création du moteur SQLite (echo=False pour ne pas afficher le SQL)
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

    print("📝 Création des tables...")
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées")

    session = get_session()

    try:
        # Employé admin
        print("👤 Vérification admin...")
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
            print("✅ Admin créé")
        else:
            admin = session.query(Employee).filter_by(_isAdmin=True).first()
            print("ℹ️  Admin existe déjà")

        # Auteur
        print("✍️  Vérification auteur...")
        if not session.query(Author).filter_by(_nickName="Edmond Rostand").first():
            admin.addAuthor(
                session=session,
                firstName="Edmond",
                lastName="Rostand",
                birthDate=date(1868, 4, 1),
                nickname="Edmond Rostand"
            )
            print("✅ Auteur créé")
        else:
            print("ℹ️  Auteur existe déjà")

        # Éditeur
        print("🏢 Vérification éditeur...")
        if not session.query(Publisher).filter_by(_name="Fasquelle").first():
            admin.addPublisher(
                session=session,
                name="Fasquelle",
                location="Paris, France",
                creationDate=date(1897, 1, 1)
            )
            print("✅ Éditeur créé")
        else:
            print("ℹ️  Éditeur existe déjà")

        # Livre
        print("📚 Vérification livre...")
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
            print("✅ Livre créé")
        else:
            print("ℹ️  Livre existe déjà")

        # Créer quelques clients de test
        print("👥 Vérification clients de test...")
        test_customers = [
            {"firstname": "Jean", "lastname": "Dupont", "email": "jean.dupont@email.com", "birthdate": date(1985, 3, 15)},
            {"firstname": "Sophie", "lastname": "Martin", "email": "sophie.martin@email.com", "birthdate": date(1990, 7, 22)},
            {"firstname": "Pierre", "lastname": "Bernard", "email": "pierre.bernard@email.com", "birthdate": date(1988, 11, 8)},
        ]

        for customer_data in test_customers:
            if not session.query(Customer).filter_by(_email=customer_data["email"]).first():
                admin.registerCustomer(
                    session=session,
                    firstName=customer_data["firstname"],
                    lastName=customer_data["lastname"],
                    email=customer_data["email"],
                    birthDate=customer_data["birthdate"]
                )
                print(f"  ✅ Client {customer_data['firstname']} {customer_data['lastname']} créé")
            else:
                print(f"  ℹ️  Client {customer_data['firstname']} {customer_data['lastname']} existe déjà")

        session.commit()
        print(f"\n✅ Initialisation terminée !")
        print(f"📊 Base de données : {DB_PATH}")

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        session.close()


print("INITIALISATION DE LA BASE DE DONNÉES")
