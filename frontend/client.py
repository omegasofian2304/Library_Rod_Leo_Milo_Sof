import customtkinter as ctk
import re

# Base de données des clients (simulée)
Clients_data = [
    {"id": 1, "nom": "Dupont", "prenom": "Jean", "email": "jean.dupont@email.com"},
    {"id": 2, "nom": "Martin", "prenom": "Sophie", "email": "sophie.martin@email.com"},
    {"id": 3, "nom": "Bernard", "prenom": "Pierre", "email": "pierre.bernard@email.com"},
    {"id": 4, "nom": "Dubois", "prenom": "Marie", "email": "marie.dubois@email.com"}
]

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
        self.win.geometry("900x650")
        title = "Modifier un client" if self.is_edit else "Créer un nouveau client"
        self.win.title(title)

        # Header
        fr_header = ctk.CTkFrame(self.win, fg_color="#B8B8B8", corner_radius=15, height=80)
        fr_header.pack(fill="x", padx=20, pady=20)

        lbl_title = ctk.CTkLabel(
            fr_header,
            text=title,
            font=("Arial", 24, "bold")
        )
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
        lbl_id = ctk.CTkLabel(fr_fields, text="ID :", font=("Arial", 14, "bold"))
        lbl_id.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        self.entry_id = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_id.grid(row=0, column=1, padx=20, pady=15)
        if self.is_edit:
            self.entry_id.configure(state="disabled")

        # Nom
        lbl_nom = ctk.CTkLabel(fr_fields, text="NOM :", font=("Arial", 14, "bold"))
        lbl_nom.grid(row=1, column=0, sticky="w", padx=20, pady=15)
        self.entry_nom = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_nom.grid(row=1, column=1, padx=20, pady=15)

        # Prénom
        lbl_prenom = ctk.CTkLabel(fr_fields, text="PRÉNOM :", font=("Arial", 14, "bold"))
        lbl_prenom.grid(row=2, column=0, sticky="w", padx=20, pady=15)
        self.entry_prenom = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_prenom.grid(row=2, column=1, padx=20, pady=15)

        # Email
        lbl_email = ctk.CTkLabel(fr_fields, text="EMAIL :", font=("Arial", 14, "bold"))
        lbl_email.grid(row=3, column=0, sticky="w", padx=20, pady=15)
        self.entry_email = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_email.grid(row=3, column=1, padx=20, pady=15)

        # Pré-remplir si modification
        if self.is_edit:
            self.entry_id.insert(0, str(self.client_data.get('id', '')))
            self.entry_nom.insert(0, self.client_data.get('nom', ''))
            self.entry_prenom.insert(0, self.client_data.get('prenom', ''))
            self.entry_email.insert(0, self.client_data.get('email', ''))

        # Boutons
        fr_buttons = ctk.CTkFrame(fr_form, fg_color="#D0D0D0")
        fr_buttons.pack(side="bottom", pady=30)

        btn_annuler = ctk.CTkButton(
            fr_buttons,
            text="ANNULER",
            fg_color=red,
            hover_color="#FF9999",
            width=180,
            height=55,
            font=("Arial", 14, "bold"),
            command=self.win.destroy
        )
        btn_annuler.pack(side="left", padx=20)

        btn_valider = ctk.CTkButton(
            fr_buttons,
            text="VALIDER",
            fg_color=green,
            hover_color="#9FD695",
            width=180,
            height=55,
            font=("Arial", 14, "bold"),
            command=self.validate
        )
        btn_valider.pack(side="right", padx=20)

        # Mettre au premier plan
        self.win.lift()
        self.win.attributes('-topmost', True)
        self.win.focus_force()
        self.win.after(100, lambda: self.win.attributes('-topmost', False))

    def validate(self):
        # Récupérer les données
        data = {
            'id': self.entry_id.get() if not self.is_edit else self.client_data.get('id'),
            'nom': self.entry_nom.get().strip(),
            'prenom': self.entry_prenom.get().strip(),
            'email': self.entry_email.get().strip()
        }

        # Validation basique
        if not data['nom'] or not data['prenom'] or not data['email']:
            self.show_error("❌ Tous les champs sont obligatoires !")
            return

        # Validation email
        if not is_valid_email(data['email']):
            self.show_error("❌ L'adresse email n'est pas valide !")
            return

        # Vérifier si l'email existe déjà (sauf pour le client en cours de modification)
        for client in Clients_data:
            if client['email'] == data['email'] and client['id'] != data['id']:
                self.show_error("❌ Cette adresse email est déjà utilisée !")
                return

        # Appeler le callback
        if self.on_validate:
            self.on_validate(data, is_edit=self.is_edit)

        self.win.destroy()

    def show_error(self, message):
        """Affiche un message d'erreur"""
        error_win = ctk.CTkToplevel(self.win)
        error_win.title("Erreur")
        error_win.geometry("400x150")
        ctk.CTkLabel(
            error_win,
            text=message,
            font=("Arial", 13, "bold")
        ).pack(pady=40)
        ctk.CTkButton(
            error_win,
            text="OK",
            command=error_win.destroy,
            width=100
        ).pack()
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

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#B8B8B8", height=60)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)

        # Logo section (gauche)
        logo_frame = ctk.CTkFrame(header_frame, fg_color="#A5C4D4", width=90, height=50)
        logo_frame.pack(side="left", padx=5, pady=5)
        logo_frame.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="👥\nGestion\nCLIENTS",
            font=("Arial", 9, "bold"),
            text_color="#476B89"
        )
        logo_label.pack(expand=True)

        # Menu hamburger (centre)
        menu_btn = ctk.CTkLabel(
            header_frame,
            text="☰",
            font=("Arial", 28),
            text_color="#333333",
            cursor="hand2"
        )
        menu_btn.pack(side="left", padx=30)
        menu_btn.bind("<Button-1>", lambda e: self.toggle_menu())

        # Compte section (droite)
        compte_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        compte_frame.pack(side="right", padx=10)

        compte_label = ctk.CTkLabel(
            compte_frame,
            text="Compte",
            font=("Arial", 11),
            text_color="#666666"
        )
        compte_label.pack(side="left", padx=5)

        user_icon = ctk.CTkLabel(
            compte_frame,
            text="⚫",
            font=("Arial", 14),
            text_color="#666666"
        )
        user_icon.pack(side="left")

    def create_add_button(self):
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        add_btn = ctk.CTkButton(
            btn_frame,
            text="Ajouter un nouveau client    +",
            font=("Arial", 13, "bold"),
            fg_color="#6366F1",
            hover_color="#4F46E5",
            height=35,
            corner_radius=8,
            command=self.open_create_overlay
        )
        add_btn.pack(side="right")

    def create_search_bar(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        # Search entry avec placeholder
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍  ID, NOM, PRÉNOM, EMAIL",
            fg_color="#C0C0C0",
            border_width=0,
            height=35,
            font=("Arial", 11)
        )
        search_entry.pack(fill="x")

    def create_scrollable_clients_list(self):
        # Frame principal pour la liste
        list_container = ctk.CTkFrame(self, fg_color="#A8A8A8")
        list_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame scrollable
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color="#A8A8A8",
            scrollbar_button_color="#888888",
            scrollbar_button_hover_color="#666666"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=2, pady=2)

    def refresh_clients_list(self):
        """Rafraîchit la liste des clients"""
        # Vider la liste actuelle
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Afficher tous les clients
        for client in Clients_data:
            self.add_client_card(client)

    def add_client_card(self, client):
        # Card pour chaque client
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#D0D0D0",
            corner_radius=10
        )
        card.pack(fill="x", padx=10, pady=8)

        # Frame interne avec padding
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", padx=15, pady=15)

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
        """Sauvegarde ou modifie un client"""
        if is_edit:
            # Modifier le client existant
            for i, client in enumerate(Clients_data):
                if client['id'] == data['id']:
                    Clients_data[i] = data
                    break
            print(f"✓ Client modifié : {data['prenom']} {data['nom']}")
        else:
            # Créer un nouveau client
            new_id = max([client['id'] for client in Clients_data], default=0) + 1
            data['id'] = new_id
            Clients_data.append(data)
            print(f"✓ Nouveau client créé : {data['prenom']} {data['nom']}")

        # Rafraîchir la liste
        self.refresh_clients_list()

    def delete_client(self, client_id):
        """Supprime un client"""
        global Clients_data
        Clients_data = [client for client in Clients_data if client['id'] != client_id]
        print(f"✓ Client {client_id} supprimé")
        self.refresh_clients_list()

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
                fg_color="#B6E0FF",
                corner_radius=10
            )
            self.menu_frame.place(x=20, y=90, width=300, height=240)

            # Boutons du menu
            menu_buttons = [
                ("Livres", self.on_livres_click),
                ("Clients", self.on_clients_click),
                ("Emprunt", self.on_emprunt_click),
                ("Employés", self.on_employes_click),
                ("Auteur", self.on_auteur_click),
                ("Edition", self.on_edition_click)
            ]

            # Créer une grille 2x3
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

        self.menu_frame.lift()
        self.menu_visible = True

    def hide_menu(self):
        """Cache le menu déroulant"""
        if self.menu_frame:
            self.menu_frame.place_forget()
        self.menu_visible = False

    def on_livres_click(self):
        print("Livres cliqué")
        self.hide_menu()

    def on_clients_click(self):
        print("Clients cliqué")
        self.hide_menu()

    def on_emprunt_click(self):
        print("Emprunt cliqué")
        self.hide_menu()

    def on_employes_click(self):
        print("Employés cliqué")
        self.hide_menu()

    def on_auteur_click(self):
        print("Auteur cliqué")
        self.hide_menu()

    def on_edition_click(self):
        print("Edition cliqué")
        self.hide_menu()


if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()