import customtkinter as ctk
import re
from datetime import date, datetime
import sys
import os
import subprocess
from PIL import Image

# Ajouter le chemin parent pour accéder au dossier db/
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# IMPORTANT : Importer depuis le dossier db/
from db.database import get_session
from Classes.base import Base
from Classes.person import Person
from Classes.customer import Customer
from Classes.employee import Employee
from Classes.author import Author
from Classes.publisher import Publisher
from Classes.books import Book
from Classes.borrow import Borrow

# Couleurs
green = "#B5E6AB"
red = "#FFBFBF"
light_grey = "#D9D9D9"
dark_grey = "#BFBFBF"


def is_valid_email(email):
    """Vérifie si l'email est valide"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


class ClientOverlayWindow:
    def __init__(self, parent, on_validate=None, client_data=None):
        """
        Overlay pour créer ou modifier un client
        """
        self.parent = parent
        self.on_validate = on_validate
        self.client_data = client_data or {}
        self.is_edit = client_data is not None

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.geometry("900x750")
        title = "Modifier un client" if self.is_edit else "Créer un nouveau client"
        self.win.title(title)

        # Header
        fr_header = ctk.CTkFrame(self.win, fg_color="#B8B8B8", corner_radius=15, height=80)
        fr_header.pack(fill="x", padx=20, pady=20)

        lbl_title = ctk.CTkLabel(fr_header, text=title, font=("Arial", 24, "bold"))
        lbl_title.pack(pady=25)

        # Contenu principal
        fr_content = ctk.CTkFrame(self.win, fg_color="#A8A8A8", corner_radius=15)
        fr_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        fr_form = ctk.CTkFrame(fr_content, fg_color="#D0D0D0", corner_radius=15)
        fr_form.pack(fill="both", expand=True, padx=40, pady=40)

        # Champs du formulaire
        fr_fields = ctk.CTkFrame(fr_form, fg_color="#D0D0D0")
        fr_fields.pack(expand=True, pady=30, padx=40)

        # ID (lecture seule si modification)
        if self.is_edit:
            lbl_id = ctk.CTkLabel(fr_fields, text="ID :", font=("Arial", 14, "bold"))
            lbl_id.grid(row=0, column=0, sticky="w", padx=20, pady=15)
            self.entry_id = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
            self.entry_id.grid(row=0, column=1, padx=20, pady=15)
            self.entry_id.configure(state="disabled")
            self.entry_id.insert(0, str(self.client_data.get('id', '')))
            row_offset = 1
        else:
            row_offset = 0

        # Prénom
        lbl_prenom = ctk.CTkLabel(fr_fields, text="PRÉNOM :", font=("Arial", 14, "bold"))
        lbl_prenom.grid(row=row_offset, column=0, sticky="w", padx=20, pady=15)
        self.entry_prenom = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_prenom.grid(row=row_offset, column=1, padx=20, pady=15)

        # Nom
        lbl_nom = ctk.CTkLabel(fr_fields, text="NOM :", font=("Arial", 14, "bold"))
        lbl_nom.grid(row=row_offset + 1, column=0, sticky="w", padx=20, pady=15)
        self.entry_nom = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_nom.grid(row=row_offset + 1, column=1, padx=20, pady=15)

        # Date de naissance
        lbl_birthdate = ctk.CTkLabel(fr_fields, text="DATE DE NAISSANCE :", font=("Arial", 14, "bold"))
        lbl_birthdate.grid(row=row_offset + 2, column=0, sticky="w", padx=20, pady=15)
        self.entry_birthdate = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12),
                                            placeholder_text="YYYY-MM-DD")
        self.entry_birthdate.grid(row=row_offset + 2, column=1, padx=20, pady=15)

        # Email
        lbl_email = ctk.CTkLabel(fr_fields, text="EMAIL :", font=("Arial", 14, "bold"))
        lbl_email.grid(row=row_offset + 3, column=0, sticky="w", padx=20, pady=15)
        self.entry_email = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_email.grid(row=row_offset + 3, column=1, padx=20, pady=15)

        # Pré-remplir si modification
        if self.is_edit:
            self.entry_prenom.insert(0, self.client_data.get('prenom', ''))
            self.entry_nom.insert(0, self.client_data.get('nom', ''))
            self.entry_birthdate.insert(0, self.client_data.get('birthdate', ''))
            self.entry_email.insert(0, self.client_data.get('email', ''))

        # Boutons
        fr_buttons = ctk.CTkFrame(fr_form, fg_color="#D0D0D0")
        fr_buttons.pack(side="bottom", pady=30)

        btn_annuler = ctk.CTkButton(fr_buttons, text="ANNULER", fg_color=red, hover_color="#FF9999",
                                     width=180, height=55, font=("Arial", 14, "bold"),
                                     command=self.win.destroy)
        btn_annuler.pack(side="left", padx=20)

        btn_valider = ctk.CTkButton(fr_buttons, text="VALIDER", fg_color=green, hover_color="#9FD695",
                                     width=180, height=55, font=("Arial", 14, "bold"),
                                     command=self.validate)
        btn_valider.pack(side="right", padx=20)

        # Mettre au premier plan
        self.win.lift()
        self.win.attributes('-topmost', True)
        self.win.focus_force()
        self.win.after(100, lambda: self.win.attributes('-topmost', False))

    def validate(self):
        # Récupérer les données
        data = {
            'prenom': self.entry_prenom.get().strip(),
            'nom': self.entry_nom.get().strip(),
            'birthdate': self.entry_birthdate.get().strip(),
            'email': self.entry_email.get().strip()
        }

        if self.is_edit:
            data['id'] = self.client_data.get('id')

        # Validation basique
        if not data['prenom'] or not data['nom'] or not data['email'] or not data['birthdate']:
            self.show_error("❌ Tous les champs sont obligatoires !")
            return

        # Validation email
        if not is_valid_email(data['email']):
            self.show_error("❌ L'adresse email n'est pas valide !")
            return

        # Validation de la date
        try:
            birthdate_obj = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
            data['birthdate'] = birthdate_obj
        except ValueError:
            self.show_error("❌ Format de date invalide ! Utilisez YYYY-MM-DD")
            return

        # Vérifier que la date n'est pas dans le futur
        if birthdate_obj > date.today():
            self.show_error("❌ La date de naissance ne peut pas être dans le futur !")
            return

        # Vérifier si l'email existe déjà dans la DB
        session = get_session()
        try:
            existing_customer = session.query(Customer).filter_by(_email=data['email']).first()
            if existing_customer and (not self.is_edit or existing_customer._id != data['id']):
                self.show_error("❌ Cette adresse email est déjà utilisée !")
                return
        finally:
            session.close()

        # Appeler le callback
        if self.on_validate:
            self.on_validate(data, is_edit=self.is_edit)

        self.win.destroy()

    def show_error(self, message):
        """Affiche un message d'erreur"""
        error_win = ctk.CTkToplevel(self.win)
        error_win.title("Erreur")
        error_win.geometry("400x150")
        ctk.CTkLabel(error_win, text=message, font=("Arial", 13, "bold")).pack(pady=40)
        ctk.CTkButton(error_win, text="OK", command=error_win.destroy, width=100).pack()
        error_win.lift()
        error_win.attributes('-topmost', True)


class ClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Gestion Clients")
        self.geometry("1100x650")

        # Configuration du thème
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Header
        self.create_header()

        # Bouton Ajouter
        self.create_add_button()

        # Barre de recherche
        self.create_search_bar()

        # Zone scrollable pour la liste des clients
        self.create_scrollable_clients_list()

        # Afficher les clients
        self.refresh_clients_list()

        # Menu déroulant (initialement caché)
        self.menu_frame = None
        self.menu_visible = False

    # === NAVIGATION ===
    def open_accueil(self):
        """Retourne à l'accueil"""
        print("🏠 Retour à l'accueil...")
        try:
            accueil_path = os.path.join(current_dir, "accueil.py")
            if os.path.exists(accueil_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, accueil_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, accueil_path])
                print("✅ Accueil lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {accueil_path}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

    def open_livres(self):
        """Ouvre la gestion des livres"""
        print("📚 Ouverture des livres...")
        try:
            livres_path = os.path.join(current_dir, "liste_de_livre.py")
            if os.path.exists(livres_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, livres_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, livres_path])
                print("✅ Livres lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {livres_path}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

    def open_emprunts(self):
        """Ouvre la gestion des emprunts"""
        print("📖 Ouverture des emprunts...")
        try:
            emprunts_path = os.path.join(current_dir, "emprunts.py")
            if os.path.exists(emprunts_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, emprunts_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, emprunts_path])
                print("✅ Emprunts lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {emprunts_path}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

    def open_employes(self):
        """Ouvre la gestion des employés"""
        print("💼 Ouverture des employés...")
        try:
            employes_path = os.path.join(current_dir, "employes.py")
            if os.path.exists(employes_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, employes_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, employes_path])
                print("✅ Employés lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {employes_path}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

    def open_auteurs(self):
        """Ouvre la gestion des auteurs"""
        print("✍️ Ouverture des auteurs...")
        try:
            auteurs_path = os.path.join(current_dir, "auteurs.py")
            if os.path.exists(auteurs_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, auteurs_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, auteurs_path])
                print("✅ Auteurs lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {auteurs_path}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

    def open_editeurs(self):
        """Ouvre la gestion des éditeurs"""
        print("🏢 Ouverture des éditeurs...")
        try:
            editeurs_path = os.path.join(current_dir, "editeurs.py")
            if os.path.exists(editeurs_path):
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, editeurs_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([sys.executable, editeurs_path])
                print("✅ Éditeurs lancé")
                self.after(1750, self.destroy)
            else:
                print(f"❌ Fichier non trouvé: {editeurs_path}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
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

        # Texte BETTER BOOKS
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="left", padx=10)
        ctk.CTkLabel(text_frame, text="BETTER", font=("Arial", 12, "bold"), text_color="white").pack()
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

    def create_add_button(self):
        add_frame = ctk.CTkFrame(self, fg_color="transparent")
        add_frame.pack(fill="x", padx=50, pady=(5, 0))

        btn_add = ctk.CTkButton(
            add_frame,
            text="➕ CRÉER NOUVEAU CLIENT",
            fg_color="#6366F1",
            hover_color="#4F46E5",
            height=45,
            font=("Arial", 13, "bold"),
            command=self.open_create_overlay
        )
        btn_add.pack(side="right")

    def create_search_bar(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=50, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher par ID, NOM, PRÉNOM, E-MAIL",
            height=40,
            font=("Arial", 12)
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_clients_list())

    def create_scrollable_clients_list(self):
        self.clients_scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#E8E8E8",
            corner_radius=10
        )
        self.clients_scrollable_frame.pack(fill="both", expand=True, padx=50, pady=(10, 20))

    def refresh_clients_list(self):
        """Rafraîchit la liste des clients depuis la base de données"""
        # Nettoyer la liste actuelle
        for widget in self.clients_scrollable_frame.winfo_children():
            widget.destroy()

        # Récupérer les clients depuis la DB
        session = get_session()
        try:
            customers = session.query(Customer).all()

            # Debug: afficher le nombre de clients
            print(f"📊 Nombre de clients dans la DB: {len(customers)}")

            # Filtrer selon la recherche
            search_text = self.search_entry.get().lower() if hasattr(self, 'search_entry') else ""

            filtered_customers = []
            for customer in customers:
                customer_dict = {
                    'id': customer._id,
                    'nom': customer.lastname,
                    'prenom': customer.firstname,
                    'email': customer._email,
                    'birthdate': customer.birthdate.strftime('%Y-%m-%d') if customer.birthdate else '',
                    'fine': customer._fine
                }

                if search_text:
                    if (search_text in str(customer_dict['id']).lower() or
                            search_text in customer_dict['nom'].lower() or
                            search_text in customer_dict['prenom'].lower() or
                            search_text in customer_dict['email'].lower()):
                        filtered_customers.append(customer_dict)
                else:
                    filtered_customers.append(customer_dict)

            # Afficher les clients
            if not filtered_customers:
                no_result_label = ctk.CTkLabel(
                    self.clients_scrollable_frame,
                    text="Aucun client trouvé",
                    font=("Arial", 14),
                    text_color="#666666"
                )
                no_result_label.pack(pady=50)
            else:
                for customer in filtered_customers:
                    self.create_client_card(customer)
        except Exception as e:
            print(f"❌ Erreur lors du chargement des clients: {e}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()

    def create_client_card(self, client):
        """Crée une carte pour afficher un client"""
        card_frame = ctk.CTkFrame(
            self.clients_scrollable_frame,
            fg_color="#F5F5F5",
            corner_radius=10,
            border_width=2,
            border_color="#D0D0D0"
        )
        card_frame.pack(fill="x", padx=15, pady=8)

        # Frame interne avec padding
        inner_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=15, pady=15)

        # Avatar du client (gauche)
        avatar_frame = ctk.CTkFrame(
            inner_frame,
            fg_color="#6366F1",
            width=100,
            height=100,
            corner_radius=50
        )
        avatar_frame.pack(side="left", padx=(0, 20))
        avatar_frame.pack_propagate(False)

        # Initiales
        initiales = f"{client['prenom'][0]}{client['nom'][0]}".upper()
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text=initiales,
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        avatar_label.pack(expand=True)

        # Informations du client (centre)
        info_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # Nom complet
        name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            name_frame,
            text="Nom complet :",
            font=("Arial", 13, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            name_frame,
            text=f"  {client['prenom']} {client['nom']}",
            font=("Arial", 13, "bold"),
            text_color="#333333"
        ).pack(side="left")

        # Email
        email_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            email_frame,
            text="Email :",
            font=("Arial", 12, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            email_frame,
            text=f"  {client['email']}",
            font=("Arial", 12),
            text_color="#333333"
        ).pack(side="left")

        # Date de naissance
        birth_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        birth_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            birth_frame,
            text="Date de naissance :",
            font=("Arial", 12, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            birth_frame,
            text=f"  {client['birthdate']}",
            font=("Arial", 12),
            text_color="#333333"
        ).pack(side="left")

        # ID Client
        id_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        id_frame.pack(fill="x")

        ctk.CTkLabel(
            id_frame,
            text="ID Client :",
            font=("Arial", 12, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            id_frame,
            text=f"  #{client['id']}",
            font=("Arial", 12),
            text_color="#666666"
        ).pack(side="left")

        # Afficher les amendes si > 0
        if client.get('fine', 0) > 0:
            fine_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            fine_frame.pack(fill="x", pady=(8, 0))

            ctk.CTkLabel(
                fine_frame,
                text="⚠️ Amendes :",
                font=("Arial", 12, "bold"),
                text_color="red"
            ).pack(side="left")

            ctk.CTkLabel(
                fine_frame,
                text=f"  {client['fine']} CHF",
                font=("Arial", 12, "bold"),
                text_color="red"
            ).pack(side="left")

        # Boutons d'action (droite)
        actions_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=10)

        # Bouton Modifier
        btn_edit = ctk.CTkButton(
            actions_frame,
            text="✏️ Modifier",
            width=120,
            height=35,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            font=("Arial", 11, "bold"),
            command=lambda c=client: self.open_edit_overlay(c)
        )
        btn_edit.pack(pady=5)

        # Bouton Supprimer
        btn_delete = ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            width=120,
            height=35,
            fg_color=red,
            hover_color="#FF9999",
            font=("Arial", 11, "bold"),
            command=lambda c=client: self.delete_client(c['id'])
        )
        btn_delete.pack(pady=5)

    def open_create_overlay(self):
        """Ouvre l'overlay pour créer un nouveau client"""
        overlay = ClientOverlayWindow(
            self,
            on_validate=self.save_client
        )
        overlay.show()

    def open_edit_overlay(self, client):
        """Ouvre l'overlay pour modifier un client"""
        overlay = ClientOverlayWindow(
            self,
            on_validate=self.save_client,
            client_data=client
        )
        overlay.show()

    def save_client(self, data, is_edit=False):
        """Sauvegarde ou modifie un client dans la base de données"""
        session = get_session()
        try:
            if is_edit:
                # Modifier le client existant
                customer = session.query(Customer).filter_by(_id=data['id']).first()
                if customer:
                    customer.firstname = data['prenom']
                    customer.lastname = data['nom']
                    customer.birthdate = data['birthdate']
                    customer._email = data['email']
                    session.commit()
                    print(f"✅ Client modifié : {data['prenom']} {data['nom']} (ID: {data['id']})")
                else:
                    print(f"❌ Client avec ID {data['id']} non trouvé")
            else:
                # Créer un nouveau client
                new_customer = Customer(
                    firstname=data['prenom'],
                    lastname=data['nom'],
                    birthdate=data['birthdate'],
                    _email=data['email'],
                    _fine=0
                )
                session.add(new_customer)
                session.commit()
                print(f"✅ Nouveau client créé : {data['prenom']} {data['nom']} (ID: {new_customer._id})")

            # Rafraîchir la liste
            self.refresh_clients_list()
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur lors de la sauvegarde : {e}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()

    def delete_client(self, client_id):
        """Supprime un client de la base de données"""
        session = get_session()
        try:
            customer = session.query(Customer).filter_by(_id=client_id).first()
            if customer:
                # Sauvegarder les infos avant suppression
                nom_complet = f"{customer.firstname} {customer.lastname}"
                session.delete(customer)
                session.commit()
                print(f"✅ Client supprimé : {nom_complet} (ID: {client_id})")
                self.refresh_clients_list()
            else:
                print(f"❌ Client avec ID {client_id} non trouvé")
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur lors de la suppression : {e}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()

    def toggle_menu(self):
        """Affiche ou cache le menu déroulant"""
        if self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        """Affiche le menu déroulant"""
        if self.menu_frame is None:
            # Créer le menu
            self.menu_frame = ctk.CTkFrame(
                self,
                fg_color="#FFB6C1",
                corner_radius=10,
                width=320,
                height=260
            )

            # Boutons du menu
            menu_buttons = [
                ("🏠 Accueil", self.open_accueil),
                ("📚 Livres", self.open_livres),
                ("👥 Membres", self.hide_menu),  # Déjà sur Membres
                ("📖 Emprunts", self.open_emprunts),
                ("💼 Employés", self.open_employes),
                ("✍️ Auteurs", self.open_auteurs),
                ("🏢 Éditeurs", self.open_editeurs),
            ]

            # Créer une grille 2 colonnes
            for i, (text, command) in enumerate(menu_buttons):
                row = i // 2
                col = i % 2

                btn = ctk.CTkButton(
                    self.menu_frame,
                    text=text,
                    font=("Arial", 13, "bold"),
                    fg_color="#D3D3D3",
                    text_color="#666666",
                    hover_color="#C0C0C0",
                    height=60,
                    corner_radius=8,
                    command=command
                )
                btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            # Configuration des colonnes
            self.menu_frame.grid_columnconfigure(0, weight=1)
            self.menu_frame.grid_columnconfigure(1, weight=1)

        self.menu_frame.place(x=20, y=90)
        self.menu_frame.lift()
        self.menu_visible = True

    def hide_menu(self):
        """Cache le menu déroulant"""
        if self.menu_frame:
            self.menu_frame.place_forget()
        self.menu_visible = False



app = ClientApp()
app.mainloop()