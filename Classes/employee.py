"""
Auteur : Sofian Hussein et Rodrigo Silva Riço
Date : 07.01.2026
Projet : Création du fichier qui contiendra la classe Employee
"""
from sqlalchemy import Integer, String, Float, Boolean, Date
from sqlalchemy.orm import mapped_column, Mapped, Session
from datetime import date, datetime, timedelta
from Classes.person import Person


class Employee(Person):
    __tablename__ = 'employee'
    ''' 
    Remarque : En Python, les attributs précédés d'un underscore (_) ne sont pas réellement privés.
    C'est juste une convention pour indiquer qu'ils sont destinés à un usage interne.
    Il est toujours possible d'y accéder depuis l'extérieur de la classe (ex: instance._id).
    '''

    # liste des attributs
    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _monthlySalary: Mapped[float] = mapped_column(Float, nullable=False)
    _arrivalDate: Mapped[date] = mapped_column(Date, nullable=False)
    _workPercentage: Mapped[int] = mapped_column(Integer, nullable=False)
    _isAdmin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    _email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    _password: Mapped[str] = mapped_column(String(255), nullable=False)

    # méthodes de gestion des emprunts

    def checkOutBook(self, session: Session, customerId: int, bookId: int) -> bool:
        """
        Permet à un client d'emprunter un livre
        :param session: Session SQLAlchemy
        :param customerId: ID du client
        :param bookId: ID du livre
        :return: True si l'emprunt a réussi, False sinon
        """
        from Classes.customer import Customer
        from Classes.books import Book
        from Classes.borrow import Borrow

        # Vérifier que le client existe
        customer = session.query(Customer).filter_by(_id=customerId).first()
        if not customer:
            raise ValueError("Client non trouvé")

        # Vérifier que le livre existe et est disponible
        book = session.query(Book).filter_by(_id=bookId).first()
        if not book:
            raise ValueError("Livre non trouvé")

        if book._status != "available":
            return False

        # Créer l'emprunt
        borrow = Borrow(
            _borrowDate=datetime.now().date(),
            _dueDate=date.today() + timedelta(days=30),
            _returned=False,
            book_id=bookId,
            customer_id=customerId
        )

        # Mettre à jour le statut du livre
        book._status = "borrowed"

        session.add(borrow)
        session.commit()
        return True

    def checkInBook(self, session: Session, borrowId: int) -> bool:
        """
        Retour d'un livre emprunté
        :param session: Session SQLAlchemy
        :param borrowId: ID de l'emprunt
        :return: True si le retour a réussi, False sinon
        """
        from Classes.borrow import Borrow  # ← CORRIGÉ
        from Classes.books import Book  # ← CORRIGÉ

        borrow = session.query(Borrow).filter_by(_id=borrowId).first()
        if not borrow:
            return False

        borrow._returnDate = datetime.now().date()
        borrow._returned = True

        # Remettre le livre en disponible
        book = session.query(Book).filter_by(_id=borrow.book_id).first()
        if book:
            book._status = "available"

        session.commit()
        return True

    def extendBorrow(self, session: Session, borrowId: int, newDueDate: date) -> bool:
        """
        Prolonge la durée d'un emprunt
        :param session: Session SQLAlchemy
        :param borrowId: ID de l'emprunt
        :param newDueDate: Nouvelle date d'échéance
        :return: True si la prolongation a réussi, False sinon
        """
        from Classes.borrow import Borrow  # ← CORRIGÉ

        borrow = session.query(Borrow).filter_by(_id=borrowId).first()
        if not borrow or borrow._returned:
            return False

        borrow._dueDate = newDueDate
        session.commit()
        return True

    # méthodes de gestion des clients

    def registerCustomer(self, session: Session, firstName: str, lastName: str,
                         email: str, birthDate: date):
        """
        Enregistre un nouveau client
        :param session: Session SQLAlchemy
        :param firstName: Prénom
        :param lastName: Nom
        :param email: Email
        :param birthDate: Date de naissance
        :return: Objet Customer créé
        """
        from Classes.customer import Customer  # ← CORRIGÉ

        customer = Customer(
            firstname=firstName,
            lastname=lastName,
            birthdate=birthDate,
            _email=email,
            _fine=0
        )

        session.add(customer)
        session.commit()
        return customer

    def addFine(self, session: Session, customerId: int, amount: float) -> None:
        """
        Ajoute une amende à un client
        :param session: Session SQLAlchemy
        :param customerId: ID du client
        :param amount: Montant de l'amende
        """
        from Classes.customer import Customer  # ← CORRIGÉ

        customer = session.query(Customer).filter_by(_id=customerId).first()
        if not customer:
            raise ValueError("Client non trouvé")

        customer._fine += amount
        session.commit()

    def payFine(self, session: Session, customerId: int, amount: float) -> None:
        """
        Enregistre le paiement d'une amende
        :param session: Session SQLAlchemy
        :param customerId: ID du client
        :param amount: Montant payé
        """
        from Classes.customer import Customer  # ← CORRIGÉ

        customer = session.query(Customer).filter_by(_id=customerId).first()
        if not customer:
            raise ValueError("Client non trouvé")

        customer._fine -= amount
        if customer._fine < 0:
            customer._fine = 0

        session.commit()

    # méthodes de gestion des livres

    def addBook(self, session: Session, title: str, nbPages: int, genre: str,
                summary: str, format: str, releaseDate: date, image: str,
                authorId: int, publisherId: int):
        """
        Ajoute un nouveau livre dans la base de données
        :param session: Session SQLAlchemy
        :param title: Titre du livre
        :param nbPages: Nombre de pages
        :param genre: Genre
        :param summary: Résumé
        :param format: Format (broché, relié, etc.)
        :param releaseDate: Date de sortie
        :param image: Chemin de l'image
        :param authorId: ID de l'auteur
        :param publisherId: ID de l'éditeur
        :return: Objet Book créé
        """
        from Classes.books import Book  # ← CORRIGÉ

        book = Book(
            _title=title,
            _nb_pages=nbPages,
            _genre=genre,
            _summary=summary,
            _format=format,
            _release_date=releaseDate,
            _image=image,
            _status="available",
            author_id=authorId,
            publisher_id=publisherId
        )

        session.add(book)
        session.commit()
        return book

    def removeBook(self, session: Session, bookId: int) -> bool:
        """
        Supprime un livre de la base de données
        :param session: Session SQLAlchemy
        :param bookId: ID du livre
        :return: True si la suppression a réussi, False sinon
        """
        from Classes.books import Book  # ← CORRIGÉ

        book = session.query(Book).filter_by(_id=bookId).first()
        if not book:
            return False

        session.delete(book)
        session.commit()
        return True

    # méthodes de gestion des employés (nécessite isAdmin=True)

    def addEmployee(self, session: Session, firstName: str, lastName: str,
                    email: str, birthDate: date, salary: float, role: str):
        """
        Ajoute un nouvel employé (réservé aux admins)
        :param session: Session SQLAlchemy
        :param firstName: Prénom
        :param lastName: Nom
        :param email: Email
        :param birthDate: Date de naissance
        :param salary: Salaire mensuel
        :param role: Rôle (admin, employee, etc.)
        :return: Objet Employee créé
        """
        if not self._isAdmin:
            raise PermissionError("Seuls les administrateurs peuvent ajouter des employés")

        employee = Employee(
            firstname=firstName,
            lastname=lastName,
            birthdate=birthDate,
            _email=email,
            _monthlySalary=salary,
            _arrivalDate=datetime.now().date(),
            _workPercentage=100,
            _isAdmin=(role.lower() == "admin"),
            _password="Pa$$w0rd"
        )

        session.add(employee)
        session.commit()
        return employee

    # méthodes de gestion des auteurs

    def addAuthor(self, session: Session, firstName: str, lastName: str,
                  birthDate: date, nickname: str):
        """
        Ajoute un nouvel auteur
        :param session: Session SQLAlchemy
        :param firstName: Prénom
        :param lastName: Nom
        :param birthDate: Date de naissance
        :param nickname: Pseudonyme
        :return: Objet Author créé
        """
        from Classes.author import Author  # ← CORRIGÉ

        author = Author(
            firstname=firstName,
            lastname=lastName,
            birthdate=birthDate,
            _nickName=nickname
        )

        session.add(author)
        session.commit()
        return author

    # méthodes de gestion des éditeurs

    def addPublisher(self, session: Session, name: str, location: str,
                     creationDate: date):
        """
        Ajoute un nouvel éditeur
        :param session: Session SQLAlchemy
        :param name: Nom de l'éditeur
        :param location: Localisation
        :param creationDate: Date de création
        :return: Objet Publisher créé
        """
        from Classes.publisher import Publisher  # ← CORRIGÉ

        publisher = Publisher(
            _name=name,
            _location=location,
            _creation_date=creationDate
        )

        session.add(publisher)
        session.commit()
        return publisher