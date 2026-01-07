import customtkinter as ctk

# Base de données des livres (simulée)
Books_data = [
    {"id": 1, "titre": "Cyrano de Bergerac", "auteur": "Edmond Rostand", "editeur": "Voir de près", "disponible": True},
    {"id": 2, "titre": "La Menace Atlante", "auteur": "Yves Sente - Peter Van Dongen", "editeur": "Blake Et Mortimer",
     "disponible": True},
    {"id": 3, "titre": "Le Petit Prince", "auteur": "Antoine de Saint-Exupéry", "editeur": "Gallimard",
     "disponible": False},
    {"id": 4, "titre": "1984", "auteur": "George Orwell", "editeur": "Penguin Books", "disponible": True}
]

# Couleurs
green = "#B5E6AB"
red = "#FFBFBF"
light_grey = "#D9D9D9"
dark_grey = "#BFBFBF"


class BookOverlayWindow:
    def __init__(self, parent, on_validate=None, book_data=None):
        """
        Overlay pour créer ou modifier un livre
        """
        self.parent = parent
        self.on_validate = on_validate
        self.book_data = book_data or {}
        self.is_edit = book_data is not None

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.geometry("900x700")
        title = "Modifier un livre" if self.is_edit else "Créer un nouveau livre"
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

        # Titre du livre
        lbl_titre = ctk.CTkLabel(fr_fields, text="TITRE :", font=("Arial", 14, "bold"))
        lbl_titre.grid(row=1, column=0, sticky="w", padx=20, pady=15)
        self.entry_titre = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_titre.grid(row=1, column=1, padx=20, pady=15)

        # Auteur
        lbl_auteur = ctk.CTkLabel(fr_fields, text="AUTEUR :", font=("Arial", 14, "bold"))
        lbl_auteur.grid(row=2, column=0, sticky="w", padx=20, pady=15)
        self.entry_auteur = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_auteur.grid(row=2, column=1, padx=20, pady=15)

        # Éditeur
        lbl_editeur = ctk.CTkLabel(fr_fields, text="ÉDITEUR :", font=("Arial", 14, "bold"))
        lbl_editeur.grid(row=3, column=0, sticky="w", padx=20, pady=15)
        self.entry_editeur = ctk.CTkEntry(fr_fields, width=450, height=45, font=("Arial", 12))
        self.entry_editeur.grid(row=3, column=1, padx=20, pady=15)

        # Disponibilité
        lbl_disponible = ctk.CTkLabel(fr_fields, text="DISPONIBLE :", font=("Arial", 14, "bold"))
        lbl_disponible.grid(row=4, column=0, sticky="w", padx=20, pady=15)
        self.check_disponible = ctk.CTkCheckBox(
            fr_fields,
            text="Livre disponible à l'emprunt",
            font=("Arial", 12),
            fg_color="#6366F1",
            hover_color="#4F46E5"
        )
        self.check_disponible.grid(row=4, column=1, sticky="w", padx=20, pady=15)

        # Pré-remplir si modification
        if self.is_edit:
            self.entry_id.insert(0, str(self.book_data.get('id', '')))
            self.entry_titre.insert(0, self.book_data.get('titre', ''))
            self.entry_auteur.insert(0, self.book_data.get('auteur', ''))
            self.entry_editeur.insert(0, self.book_data.get('editeur', ''))
            if self.book_data.get('disponible', False):
                self.check_disponible.select()

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
            'id': self.entry_id.get() if not self.is_edit else self.book_data.get('id'),
            'titre': self.entry_titre.get().strip(),
            'auteur': self.entry_auteur.get().strip(),
            'editeur': self.entry_editeur.get().strip(),
            'disponible': self.check_disponible.get() == 1
        }

        # Validation basique
        if not data['titre'] or not data['auteur'] or not data['editeur']:
            error_win = ctk.CTkToplevel(self.win)
            error_win.title("Erreur")
            error_win.geometry("300x150")
            ctk.CTkLabel(
                error_win,
                text="❌ Tous les champs sont obligatoires !",
                font=("Arial", 13, "bold")
            ).pack(pady=40)
            ctk.CTkButton(
                error_win,
                text="OK",
                command=error_win.destroy,
                width=100
            ).pack()
            return

        # Appeler le callback
        if self.on_validate:
            self.on_validate(data, is_edit=self.is_edit)

        self.win.destroy()


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Gestion Bibliothèque")
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

        # Checkbox disponible
        self.create_availability_checkbox()

        # Zone scrollable pour la liste des livres
        self.create_scrollable_books_list()

        # Afficher les livres
        self.refresh_books_list()

        # Menu déroulant (initialement caché)
        self.menu_frame = None
        self.menu_visible = False

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#B8B8B8", height=60)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)

        # Logo section (gauche)
        logo_frame = ctk.CTkFrame(header_frame, fg_color="#D4A5C4", width=90, height=50)
        logo_frame.pack(side="left", padx=5, pady=5)
        logo_frame.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="📚\nGestion\nBOOKS",
            font=("Arial", 9, "bold"),
            text_color="#8B4789"
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
            text="Ajouter un nouveau livre    +",
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
            placeholder_text="🔍  ID, TITRE, AUTEUR, EDITEUR",
            fg_color="#C0C0C0",
            border_width=0,
            height=35,
            font=("Arial", 11)
        )
        search_entry.pack(fill="x")

    def create_availability_checkbox(self):
        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(fill="x", padx=10, pady=5)

        checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="disponible",
            font=("Arial", 11),
            fg_color="#6366F1",
            hover_color="#4F46E5"
        )
        checkbox.pack(anchor="w")

    def create_scrollable_books_list(self):
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

    def refresh_books_list(self):
        """Rafraîchit la liste des livres"""
        # Vider la liste actuelle
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Afficher tous les livres
        for book in Books_data:
            self.add_book_card(book)

    def add_book_card(self, book):
        # Card pour chaque livre
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#D0D0D0",
            corner_radius=10
        )
        card.pack(fill="x", padx=10, pady=8)

        # Frame interne avec padding
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", padx=15, pady=15)

        # Couverture du livre (gauche)
        cover_frame = ctk.CTkFrame(
            inner_frame,
            fg_color="white",
            width=80,
            height=120,
            corner_radius=5
        )
        cover_frame.pack(side="left", padx=(0, 20))
        cover_frame.pack_propagate(False)

        cover_icons = ["📕", "📘", "📗", "📙", "📔"]
        cover_text = cover_icons[book['id'] % len(cover_icons)]

        cover_label = ctk.CTkLabel(
            cover_frame,
            text=cover_text,
            font=("Arial", 40)
        )
        cover_label.pack(expand=True)

        # Informations du livre (centre)
        info_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # Titre
        title_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            title_frame,
            text="Titre :",
            font=("Arial", 13, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text=f"  {book['titre']}",
            font=("Arial", 13, "bold"),
            text_color="#333333"
        ).pack(side="left")

        # Éditeur
        editor_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        editor_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            editor_frame,
            text="Editeur :",
            font=("Arial", 12, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            editor_frame,
            text=f"  {book['editeur']}",
            font=("Arial", 12),
            text_color="#333333"
        ).pack(side="left")

        # Auteur
        author_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        author_frame.pack(fill="x")

        ctk.CTkLabel(
            author_frame,
            text="Auteur :",
            font=("Arial", 12, "bold"),
            text_color="#555555"
        ).pack(side="left")

        ctk.CTkLabel(
            author_frame,
            text=f"  {book['auteur']}",
            font=("Arial", 12),
            text_color="#333333"
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
            command=lambda b=book: self.open_edit_overlay(b)
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
            command=lambda b=book: self.delete_book(b['id'])
        )
        btn_delete.pack(pady=5)

        # Badge disponibilité
        if book.get('disponible', True):
            badge = ctk.CTkLabel(
                actions_frame,
                text="✓ Disponible",
                font=("Arial", 10, "bold"),
                text_color="green"
            )
        else:
            badge = ctk.CTkLabel(
                actions_frame,
                text="✗ Emprunté",
                font=("Arial", 10, "bold"),
                text_color="red"
            )
        badge.pack(pady=5)

    def open_create_overlay(self):
        """Ouvre l'overlay pour créer un nouveau livre"""
        overlay = BookOverlayWindow(
            self,
            on_validate=self.save_book
        )
        overlay.show()

    def open_edit_overlay(self, book):
        """Ouvre l'overlay pour modifier un livre"""
        overlay = BookOverlayWindow(
            self,
            on_validate=self.save_book,
            book_data=book
        )
        overlay.show()

    def save_book(self, data, is_edit=False):
        """Sauvegarde ou modifie un livre"""
        if is_edit:
            # Modifier le livre existant
            for i, book in enumerate(Books_data):
                if book['id'] == data['id']:
                    Books_data[i] = data
                    break
            print(f"✓ Livre modifié : {data['titre']}")
        else:
            # Créer un nouveau livre
            new_id = max([book['id'] for book in Books_data], default=0) + 1
            data['id'] = new_id
            Books_data.append(data)
            print(f"✓ Nouveau livre créé : {data['titre']}")

        # Rafraîchir la liste
        self.refresh_books_list()

    def delete_book(self, book_id):
        """Supprime un livre"""
        global Books_data
        Books_data = [book for book in Books_data if book['id'] != book_id]
        print(f"✓ Livre {book_id} supprimé")
        self.refresh_books_list()

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
                corner_radius=10
            )
            self.menu_frame.place(x=20, y=90, width=300, height=240)

            # Boutons du menu
            menu_buttons = [
                ("Livres", self.on_livres_click),
                ("Membres", self.on_membres_click),
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

    def on_membres_click(self):
        print("Membres cliqué")
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
    app = LibraryApp()
    app.mainloop()