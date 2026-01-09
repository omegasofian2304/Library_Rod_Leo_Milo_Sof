import customtkinter as ctk
from PIL import Image
import sys
import os
import subprocess

# Ajouter le chemin parent pour accéder au dossier db/
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# IMPORTANT : Importer TOUTES les classes pour résoudre les relations SQLAlchemy
from db.database import get_session
from Classes.base import Base
from Classes.person import Person
from Classes.customer import Customer
from Classes.employee import Employee
from Classes.author import Author
from Classes.publisher import Publisher
from Classes.books import Book
from Classes.borrow import Borrow


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion Bibliothèque")
        self.geometry("1100x700")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Récupérer le livre recommandé
        self.recommended_book = self.get_recommended_book()

        self.create_header()
        self.create_recommendation_section()

        self.menu_frame = None
        self.menu_visible = False

    def get_recommended_book(self):
        """Récupère le livre avec l'ID 1 depuis la base de données"""
        session = get_session()
        try:
            book = session.query(Book).filter_by(_id=1).first()

            if book:
                # Récupérer le nom de l'auteur
                author_name = "N/A"
                try:
                    if hasattr(book, 'author') and book.author:
                        author_name = f"{book.author.firstname} {book.author.lastname}"
                except Exception as author_error:
                    print(f"⚠️ Erreur auteur: {author_error}")

                # Récupérer le nom de l'éditeur
                publisher_name = "N/A"
                try:
                    if hasattr(book, 'publisher') and book.publisher:
                        publisher_name = book.publisher._name
                except Exception as pub_error:
                    print(f"⚠️ Erreur éditeur: {pub_error}")

                print(f"✅ Livre chargé: {book._title} par {author_name}")

                return {
                    'title': book._title,
                    'publisher': publisher_name,
                    'author': author_name,
                    'pages': book._nb_pages,
                    'genre': book._genre,
                    'summary': book._summary,
                    'format': book._format,
                    'image': book._image
                }
            else:
                print("⚠️ Aucun livre avec ID=1")
                return {
                    'title': "Aucun livre",
                    'publisher': "N/A",
                    'author': "N/A",
                    'pages': 0,
                    'genre': "N/A",
                    'summary': "Aucune recommandation disponible",
                    'format': "N/A",
                    'image': None
                }
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du livre: {e}")
            import traceback
            traceback.print_exc()
            return {
                'title': "Erreur",
                'publisher': "N/A",
                'author': "N/A",
                'pages': 0,
                'genre': "N/A",
                'summary': "Impossible de charger les données",
                'format': "N/A",
                'image': None
            }
        finally:
            session.close()

    # === NAVIGATION ===
    def open_livres(self):
        """Ouvre la fenêtre de gestion des livres"""
        print("📚 Ouverture de la gestion des livres...")
        try:
            livres_path = os.path.join(current_dir, "liste_de_livre.py")
            if os.path.exists(livres_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, livres_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, livres_path])
                print("✅ Processus liste_de_livre.py lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {livres_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture: {e}")
            import traceback
            traceback.print_exc()

    def open_membres(self):
        """Ouvre la fenêtre de gestion des membres"""
        print("📂 Ouverture de la gestion des membres...")
        try:
            client_path = os.path.join(current_dir, "client.py")
            if os.path.exists(client_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, client_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, client_path])
                print("✅ Processus client.py lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {client_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture: {e}")
            import traceback
            traceback.print_exc()

    def open_emprunts(self):
        """Ouvre la fenêtre de gestion des emprunts"""
        print("📖 Ouverture de la gestion des emprunts...")
        try:
            emprunts_path = os.path.join(current_dir, "emprunts.py")
            if os.path.exists(emprunts_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, emprunts_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, emprunts_path])
                print("✅ Processus emprunts.py lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {emprunts_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture: {e}")
            import traceback
            traceback.print_exc()

    def open_employes(self):
        """Ouvre la fenêtre de gestion des employés"""
        print("💼 Ouverture de la gestion des employés...")
        try:
            employes_path = os.path.join(current_dir, "employes.py")
            if os.path.exists(employes_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, employes_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, employes_path])
                print("✅ Processus employes.py lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {employes_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture: {e}")
            import traceback
            traceback.print_exc()

    def open_auteurs(self):
        """Ouvre la fenêtre de gestion des auteurs"""
        print("✍️ Ouverture de la gestion des auteurs...")
        try:
            auteurs_path = os.path.join(current_dir, "auteurs.py")
            if os.path.exists(auteurs_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, auteurs_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, auteurs_path])
                print("✅ Processus auteurs.py lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {auteurs_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture: {e}")
            import traceback
            traceback.print_exc()

    def open_editeurs(self):
        """Ouvre la fenêtre de gestion des éditeurs"""
        print("🏢 Ouverture de la gestion des éditeurs...")
        try:
            editeurs_path = os.path.join(current_dir, "editeurs.py")
            if os.path.exists(editeurs_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, editeurs_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, editeurs_path])
                print("✅ Processus editeurs.py lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {editeurs_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture: {e}")
            import traceback
            traceback.print_exc()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#FFB6C1", height=60)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(header_frame, fg_color="#7C3AED", width=60, height=50, corner_radius=10)
        logo_frame.pack(side="left", padx=5, pady=5)
        logo_frame.pack_propagate(False)

        try:
            logo_path = os.path.join(parent_dir, "img", "logo.png")
            logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(50, 50)
            )
            ctk.CTkLabel(logo_frame, image=logo_image, text="").pack(expand=True)
        except:
            ctk.CTkLabel(logo_frame, text="📚", font=("Arial", 40)).pack(expand=True)

        # Texte Magicbooks
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="left", padx=10)
        ctk.CTkLabel(text_frame, text="MAGIC", font=("Arial", 12, "bold"), text_color="white").pack()
        ctk.CTkLabel(text_frame, text="BOOKS", font=("Arial", 12, "bold"), text_color="white").pack()

        # Menu hamburger
        menu_btn = ctk.CTkLabel(header_frame, text="☰", font=("Arial", 28), text_color="#333333", cursor="hand2")
        menu_btn.pack(side="left", padx=30)
        menu_btn.bind("<Button-1>", lambda e: self.toggle_menu())

        # Compte section
        compte_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        compte_frame.pack(side="right", padx=10)
        ctk.CTkLabel(compte_frame, text="Compte", font=("Arial", 11), text_color="#666666").pack(side="left", padx=5)
        ctk.CTkLabel(compte_frame, text="👤", font=("Arial", 14)).pack(side="left")

    def create_recommendation_section(self):
        reco_frame = ctk.CTkFrame(self, fg_color="#6C5CE7", corner_radius=10)
        reco_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(reco_frame, text="Recommandation de la semaine :", font=("Arial", 18, "bold"),
                     text_color="white").pack(padx=20, pady=10)

        content = ctk.CTkFrame(reco_frame, fg_color="#e6c39f", corner_radius=15)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Image du livre
        image_frame = ctk.CTkFrame(content, width=300, height=420, fg_color="#ffffff", corner_radius=10)
        image_frame.pack(side="left", padx=30, pady=30)
        image_frame.pack_propagate(False)

        # Charger l'image du livre
        image_loaded = False
        if self.recommended_book['image']:
            possible_paths = [
                self.recommended_book['image'],
                os.path.join(current_dir, self.recommended_book['image']),
                os.path.join(parent_dir, self.recommended_book['image']),
                os.path.join(current_dir, "img", "Cyrano-de-Bergerac.jpg"),
                os.path.join(parent_dir, "img", "Cyrano-de-Bergerac.jpg"),
            ]

            for img_path in possible_paths:
                try:
                    if os.path.exists(img_path):
                        print(f"📸 Image trouvée: {img_path}")
                        pil_image = Image.open(img_path)
                        book_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(280, 400))
                        lbl_image = ctk.CTkLabel(image_frame, image=book_image, text="")
                        lbl_image.image = book_image
                        lbl_image.pack(expand=True)
                        image_loaded = True
                        break
                except Exception as e:
                    continue

        if not image_loaded:
            ctk.CTkLabel(image_frame, text="📖\nCyrano de Bergerac\n\nImage non disponible",
                        font=("Arial", 14), justify="center").pack(expand=True)

        # Informations texte
        info_frame = ctk.CTkFrame(content, fg_color="#e6c39f")
        info_frame.pack(side="left", padx=20, pady=30, fill="both", expand=True)

        book_info = [
            ("Titre :", self.recommended_book['title']),
            ("Éditeur :", self.recommended_book['publisher']),
            ("Auteur :", self.recommended_book['author']),
            ("Genre :", self.recommended_book['genre']),
            ("Pages :", str(self.recommended_book['pages'])),
            ("Format :", self.recommended_book['format'])
        ]

        for label_text, value_text in book_info:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=8)
            ctk.CTkLabel(row_frame, text=label_text, font=("Arial", 20, "bold")).pack(side="left")
            ctk.CTkLabel(row_frame, text=value_text, font=("Arial", 20)).pack(side="left", padx=15)

        # Résumé
        summary_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        summary_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(summary_frame, text="Résumé :", font=("Arial", 18, "bold")).pack(anchor="w")
        ctk.CTkLabel(summary_frame, text=self.recommended_book['summary'],
                     font=("Arial", 14), wraplength=400, justify="left").pack(anchor="w", pady=5)

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.place_forget()
            self.menu_visible = False
        else:
            self.show_menu()

    def show_menu(self):
        if self.menu_frame is None:
            self.menu_frame = ctk.CTkFrame(self, fg_color="#FFB6C1", corner_radius=10, width=320, height=260)

            menu_buttons = [
                ("🏠 Accueil", lambda: self.hide_menu()),
                ("📚 Livres", self.open_livres),
                ("👥 Membres", self.open_membres),
                ("📖 Emprunts", self.open_emprunts),
                ("💼 Employés", self.open_employes),
                ("✍️ Auteurs", self.open_auteurs),
                ("🏢 Éditeurs", self.open_editeurs),
            ]

            for i, (text, command) in enumerate(menu_buttons):
                row = i // 2
                col = i % 2
                btn = ctk.CTkButton(self.menu_frame, text=text, font=("Arial", 13, "bold"),
                                    fg_color="#D3D3D3", text_color="#666666",
                                    hover_color="#C0C0C0", height=60, corner_radius=8,
                                    command=command)
                btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            self.menu_frame.grid_columnconfigure(0, weight=1)
            self.menu_frame.grid_columnconfigure(1, weight=1)

        self.menu_frame.place(x=20, y=90)
        self.menu_frame.lift()
        self.menu_visible = True

    def hide_menu(self):
        if self.menu_frame:
            self.menu_frame.place_forget()
            self.menu_visible = False



app = LibraryApp()
app.mainloop()