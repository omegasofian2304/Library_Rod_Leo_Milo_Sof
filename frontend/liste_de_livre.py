import customtkinter as ctk


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

        # Ajouter des livres d'exemple
        self.add_sample_books()

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
            corner_radius=8
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

    def add_book_card(self, title, author, editor, cover_text="📖"):
        # Card pour chaque livre
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#D0D0D0",
            corner_radius=10
        )
        card.pack(fill="x", padx=10, pady=8)

        # Frame interne avec padding
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="x", padx=15, pady=15)

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

        cover_label = ctk.CTkLabel(
            cover_frame,
            text=cover_text,
            font=("Arial", 40)
        )
        cover_label.pack(expand=True)

        # Informations du livre (droite)
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
            text=f"  {title}",
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
            text=f"  {editor}",
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
            text=f"  {author}",
            font=("Arial", 12),
            text_color="#333333"
        ).pack(side="left")

    def add_sample_books(self):
        # Livre 1
        self.add_book_card(
            title="Cyrano de Bergerac",
            author="Edmond Rostand",
            editor="Voir de près",
            cover_text="📕"
        )

        # Livre 2
        self.add_book_card(
            title="La Menace Atlante",
            author="Yves Sente - Peter Van Dongen",
            editor="Blake Et Mortimer",
            cover_text="📘"
        )

        # Livres supplémentaires pour démontrer le scroll
        self.add_book_card(
            title="Le Petit Prince",
            author="Antoine de Saint-Exupéry",
            editor="Gallimard",
            cover_text="📗"
        )

        self.add_book_card(
            title="1984",
            author="George Orwell",
            editor="Penguin Books",
            cover_text="📙"
        )

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
                width=300,
                height=240
            )

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

            # Configuration des colonnes pour qu'elles aient la même largeur
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