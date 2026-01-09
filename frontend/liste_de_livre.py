import subprocess
import customtkinter as ctk
import sys
import os
from datetime import datetime
from PIL import Image

# === Initialisation chemin & imports DB (mêmes patterns que accueil.py) ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# IMPORTANT : importer toutes les classes pour résoudre les relations SQLAlchemy
from db.database import get_session
from Classes.base import Base
from Classes.person import Person
from Classes.customer import Customer
from Classes.employee import Employee
from Classes.author import Author
from Classes.publisher import Publisher
from Classes.books import Book
from Classes.borrow import Borrow

# Couleurs (alignées sur accueil.py)
PALE_GREEN = "#B5E6AB"
PALE_GREEN_HOVER = "#9FD695"
PALE_RED = "#FFBFBF"
PALE_RED_HOVER = "#FF9999"

COLOR_HEADER = "#FFB6C1"   # ← était #B8B8B8, on aligne sur accueil.py
COLOR_CONTENT = "#A8A8A8"
COLOR_FORM = "#D0D0D0"

def _label_for_author(a: Author) -> str:
    """Étiquette pour l'auteur (nick + nom/prénom si dispo)."""
    fn = getattr(a, "firstname", "") or ""
    ln = getattr(a, "lastname", "") or ""
    nick = getattr(a, "_nickName", "") or ""
    if nick and (fn or ln):
        return f"[{nick}] {fn} {ln}".strip()
    if fn or ln:
        return f"{fn} {ln}".strip()
    return nick or f"Auteur #{getattr(a, '_id', '?')}"

def _label_for_publisher(p: Publisher) -> str:
    name = getattr(p, "_name", "") or ""
    return name or f"Éditeur #{getattr(p, '_id', '?')}"

# ---------- Popup d'ajout/édition de livre ----------
class BookOverlayWindow:
    """
    Popup d'ajout/édition avec:
    - zone scrollable pour le formulaire
    - barre fixe en bas avec ANNULER (rouge pâle) et VALIDER (vert pâle)
    - style visuel aligné
    """
    def __init__(self, parent, on_validate=None, book_data=None):
        self.parent = parent
        self.on_validate = on_validate
        self.book_data = book_data or {}
        self.is_edit = book_data is not None

        # Sources ComboBox
        self.author_labels = []
        self.author_id_by_label = {}
        self.publisher_labels = []
        self.publisher_id_by_label = {}

        # Liste de statuts
        self.status_choices = ["available", "borrowed", "reserved", "lost", "damaged"]

    # --- Master data (Auteurs / Éditeurs) ---
    def _load_master_data(self) -> bool:
        session = get_session()
        try:
            authors = session.query(Author).order_by(Author._id.asc()).all()
            publishers = session.query(Publisher).order_by(Publisher._id.asc()).all()

            self.author_labels.clear()
            self.author_id_by_label.clear()
            for a in authors:
                lbl = _label_for_author(a)
                self.author_labels.append(lbl)
                self.author_id_by_label[lbl] = getattr(a, "_id", None)

            self.publisher_labels.clear()
            self.publisher_id_by_label.clear()
            for p in publishers:
                lbl = _label_for_publisher(p)
                self.publisher_labels.append(lbl)
                self.publisher_id_by_label[lbl] = getattr(p, "_id", None)

            return bool(self.author_labels) and bool(self.publisher_labels)
        except Exception as e:
            print(f"❌ Erreur chargement master data: {e}")
            import traceback; traceback.print_exc()
            return False
        finally:
            session.close()

    # --- UI ---
    def show(self):
        # Charger Auteurs/Éditeurs avant d'ouvrir
        if not self._load_master_data():
            self._show_error(
                "❌ Aucun auteur ou éditeur trouvé dans la base.\n"
                "Créez-les d'abord avant d'ajouter un livre."
            )
            return

        self.win = ctk.CTkToplevel(self.parent)
        self.win.title("Modifier un livre" if self.is_edit else "Ajouter un nouveau livre")
        self.win.geometry("980x820")
        self.win.minsize(820, 620)
        self.win.resizable(True, True)

        # HEADER
        fr_header = ctk.CTkFrame(self.win, fg_color=COLOR_HEADER, corner_radius=15, height=80)
        fr_header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(fr_header, text=self.win.title(), font=("Arial", 24, "bold")).pack(pady=25)

        # CONTENT
        fr_content = ctk.CTkFrame(self.win, fg_color=COLOR_CONTENT, corner_radius=15)
        fr_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # FORM CONTAINER
        fr_form = ctk.CTkFrame(fr_content, fg_color=COLOR_FORM, corner_radius=15)
        fr_form.pack(fill="both", expand=True, padx=40, pady=40)

        # Zone scrollable
        fr_scroll = ctk.CTkScrollableFrame(
            fr_form, fg_color=COLOR_FORM, corner_radius=0,
            scrollbar_button_color="#888888", scrollbar_button_hover_color="#666666",
            width=820, height=520
        )
        fr_scroll.pack(side="top", fill="both", expand=True, padx=0, pady=(0, 12))

        # Sous-frame pour placer les champs
        fr_fields = ctk.CTkFrame(fr_scroll, fg_color=COLOR_FORM)
        fr_fields.pack(fill="x", expand=False, padx=20, pady=20)

        row = 0
        # ID (lecture seule en modif)
        ctk.CTkLabel(fr_fields, text="ID :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=10
        )
        self.entry_id = ctk.CTkEntry(fr_fields, width=250, height=40, font=("Arial", 12))
        self.entry_id.grid(row=row, column=1, padx=20, pady=10, sticky="w")
        if self.is_edit:
            self.entry_id.insert(0, str(self.book_data.get("id", "")))
            self.entry_id.configure(state="disabled")
        row += 1

        # Titre (≤200)
        ctk.CTkLabel(fr_fields, text="TITRE (≤200) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_titre = ctk.CTkEntry(fr_fields, width=540, height=40, font=("Arial", 12))
        self.entry_titre.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Auteur (ComboBox)
        ctk.CTkLabel(fr_fields, text="AUTEUR :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.combo_author = ctk.CTkComboBox(fr_fields, values=self.author_labels, width=340)
        self.combo_author.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        if self.author_labels:
            self.combo_author.set(self.author_labels[0])
        row += 1

        # Éditeur (ComboBox)
        ctk.CTkLabel(fr_fields, text="ÉDITEUR :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.combo_publisher = ctk.CTkComboBox(fr_fields, values=self.publisher_labels, width=340)
        self.combo_publisher.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        if self.publisher_labels:
            self.combo_publisher.set(self.publisher_labels[0])
        row += 1

        # Genre (≤25)
        ctk.CTkLabel(fr_fields, text="GENRE (≤25) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_genre = ctk.CTkEntry(fr_fields, width=340, height=40, font=("Arial", 12))
        self.entry_genre.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Nb pages (int > 0)
        ctk.CTkLabel(fr_fields, text="NOMBRE DE PAGES :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_pages = ctk.CTkEntry(fr_fields, width=180, height=40, font=("Arial", 12))
        self.entry_pages.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Format (≤15)
        ctk.CTkLabel(fr_fields, text="FORMAT (≤15) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_format = ctk.CTkEntry(fr_fields, width=240, height=40, font=("Arial", 12))
        self.entry_format.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Date de sortie (YYYY-MM-DD)
        ctk.CTkLabel(fr_fields, text="DATE DE SORTIE (YYYY-MM-DD) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_release = ctk.CTkEntry(fr_fields, width=240, height=40, font=("Arial", 12))
        self.entry_release.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Image (chemin ≤200)
        ctk.CTkLabel(fr_fields, text="IMAGE (chemin, ≤200) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_image = ctk.CTkEntry(fr_fields, width=540, height=40, font=("Arial", 12))
        self.entry_image.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Résumé (≤200)
        ctk.CTkLabel(fr_fields, text="RÉSUMÉ (≤200) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="nw", padx=20, pady=8
        )
        self.txt_summary = ctk.CTkTextbox(fr_fields, width=540, height=140, font=("Arial", 12))
        self.txt_summary.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Statut (ComboBox)
        ctk.CTkLabel(fr_fields, text="STATUT :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.combo_status = ctk.CTkComboBox(fr_fields, values=self.status_choices, width=240)
        self.combo_status.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        self.combo_status.set(self.status_choices[0])
        row += 1

        # Pré-remplissage en édition
        if self.is_edit:
            self.entry_titre.insert(0, self.book_data.get("titre", ""))
            self.entry_genre.insert(0, self.book_data.get("genre", ""))
            pages = self.book_data.get("pages")
            if pages is not None:
                self.entry_pages.insert(0, str(pages))
            self.entry_format.insert(0, self.book_data.get("format", ""))
            self.entry_release.insert(0, self.book_data.get("release_date", "") or "")
            self.entry_image.insert(0, self.book_data.get("image", "") or "")
            self.txt_summary.insert("1.0", self.book_data.get("summary", "") or "")
            self.combo_status.set(self.book_data.get("status", self.status_choices[0]))

            # Sélectionner l'auteur/éditeur
            aid = self.book_data.get("author_id")
            pid = self.book_data.get("publisher_id")
            for lbl, _id in self.author_id_by_label.items():
                if _id == aid:
                    self.combo_author.set(lbl)
                    break
            for lbl, _id in self.publisher_id_by_label.items():
                if _id == pid:
                    self.combo_publisher.set(lbl)
                    break

        # BARRE DES BOUTONS (fixe en bas, toujours visible)
        fr_buttons = ctk.CTkFrame(fr_form, fg_color=COLOR_FORM)
        fr_buttons.pack(side="bottom", fill="x", padx=20, pady=(4, 14))
        ctk.CTkButton(
            fr_buttons, text="ANNULER",
            fg_color=PALE_RED, hover_color=PALE_RED_HOVER,
            width=180, height=50, font=("Arial", 14, "bold"),
            command=self.win.destroy
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            fr_buttons, text="VALIDER",
            fg_color=PALE_GREEN, hover_color=PALE_GREEN_HOVER,
            width=180, height=50, font=("Arial", 14, "bold"),
            command=self.validate
        ).pack(side="right", padx=10)

        # Topmost
        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.focus_force()
        self.win.after(120, lambda: self.win.attributes("-topmost", False))

    # Validation
    def validate(self):
        data = {
            "id": self.book_data.get("id") if self.is_edit else None,
            "titre": self.entry_titre.get().strip(),
            "author_label": self.combo_author.get().strip(),
            "publisher_label": self.combo_publisher.get().strip(),
            "genre": self.entry_genre.get().strip(),
            "pages": self.entry_pages.get().strip(),
            "format": self.entry_format.get().strip(),
            "release_date": self.entry_release.get().strip(),
            "image": self.entry_image.get().strip(),
            "summary": self.txt_summary.get("1.0", "end").strip(),
            "status": self.combo_status.get().strip(),
        }

        # Champs obligatoires
        required = [
            "titre", "author_label", "publisher_label", "genre", "pages",
            "format", "release_date", "image", "summary", "status",
        ]
        if any(not data[k] for k in required):
            self._show_error("❌ Tous les champs sont obligatoires.")
            return

        # Longueurs max
        if len(data["titre"]) > 200:
            self._show_error("❌ Titre ≤ 200 caractères."); return
        if len(data["genre"]) > 25:
            self._show_error("❌ Genre ≤ 25 caractères."); return
        if len(data["summary"]) > 200:
            self._show_error("❌ Résumé ≤ 200 caractères."); return
        if len(data["format"]) > 15:
            self._show_error("❌ Format ≤ 15 caractères."); return
        if len(data["image"]) > 200:
            self._show_error("❌ Chemin d'image ≤ 200 caractères."); return
        if len(data["status"]) > 25:
            self._show_error("❌ Statut ≤ 25 caractères."); return

        # pages -> int+
        try:
            p = int(data["pages"])
            if p <= 0:
                raise ValueError()
            data["pages"] = p
        except Exception:
            self._show_error("❌ Le nombre de pages doit être un entier positif.")
            return

        # release_date -> date
        try:
            data["release_date"] = datetime.strptime(data["release_date"], "%Y-%m-%d").date()
        except Exception:
            self._show_error("❌ La date doit être au format YYYY-MM-DD.")
            return

        # Résoudre IDs depuis labels
        author_id = self.author_id_by_label.get(data["author_label"])
        publisher_id = self.publisher_id_by_label.get(data["publisher_label"])
        if not author_id or not publisher_id:
            self._show_error("❌ Auteur ou Éditeur introuvable.")
            return
        data["author_id"] = author_id
        data["publisher_id"] = publisher_id

        if self.on_validate:
            self.on_validate(data, is_edit=self.is_edit)
        self.win.destroy()

    # Erreur pop-in
    def _show_error(self, message: str):
        err = ctk.CTkToplevel(self.parent)
        err.title("Erreur")
        err.geometry("440x160")
        ctk.CTkLabel(err, text=message, font=("Arial", 13, "bold")).pack(pady=40)
        ctk.CTkButton(err, text="OK", command=err.destroy, width=100).pack()


# ---------- Fenêtre principale ----------
class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion Bibliothèque")
        self.geometry("1100x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.create_header()
        self.create_add_button()
        self.create_search_bar()
        self.create_availability_checkbox()
        self.create_scrollable_books_list()
        self.refresh_books_list()

        self.menu_frame = None
        self.menu_visible = False

    # Utilitaire commun pour lancer un autre écran (aligné accueil.py)
    def _spawn_like_accueil(self, script_name: str) -> bool:
        path = os.path.join(current_dir, script_name)
        if not os.path.exists(path):
            print(f"❌ Fichier non trouvé: {path}")
            return False
        try:
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, path],
                                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                subprocess.Popen([sys.executable, path])  # pas de start_new_session
            return True
        except Exception as e:
            print(f"❌ Erreur lancement {path}: {e}")
            import traceback; traceback.print_exc()
            return False

    # Header (identique à accueil.py)
    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_HEADER, height=60)
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
        except Exception:
            ctk.CTkLabel(logo_frame, text="📚", font=("Arial", 40)).pack(expand=True)

        # Texte "MAGIC / BOOKS"
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="left", padx=10)
        ctk.CTkLabel(text_frame, text="MAGIC", font=("Arial", 12, "bold"), text_color="white").pack()
        ctk.CTkLabel(text_frame, text="BOOKS", font=("Arial", 12, "bold"), text_color="white").pack()

        # Menu hamburger
        menu_btn = ctk.CTkLabel(header_frame, text="☰", font=("Arial", 28), text_color="#333333", cursor="hand2")
        menu_btn.pack(side="left", padx=30)
        menu_btn.bind("<Button-1>", lambda e: self.toggle_menu())

        # Compte (à droite)
        compte_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        compte_frame.pack(side="right", padx=10)
        ctk.CTkLabel(compte_frame, text="Compte", font=("Arial", 11), text_color="#666666").pack(side="left", padx=5)
        ctk.CTkLabel(compte_frame, text="👤", font=("Arial", 14)).pack(side="left")

    # Bouton "Ajouter"
    def create_add_button(self):
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(
            btn_frame,
            text="Ajouter un nouveau livre +",
            font=("Arial", 13, "bold"),
            fg_color="#6366F1",
            hover_color="#4F46E5",
            height=35,
            corner_radius=8,
            command=self.open_create_overlay,
        ).pack(side="right")

    # Barre de recherche
    def create_search_bar(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 ID, TITRE, AUTEUR, ÉDITEUR",
            fg_color="#C0C0C0",
            border_width=0,
            height=35,
            font=("Arial", 11),
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_books_list())

    # Checkbox "disponible"
    def create_availability_checkbox(self):
        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(fill="x", padx=10, pady=5)
        self.availability_checkbox = ctk.CTkCheckBox(
            checkbox_frame, text="disponible", font=("Arial", 11),
            fg_color="#6366F1", hover_color="#4F46E5"
        )
        self.availability_checkbox.pack(anchor="w")
        self.availability_checkbox.bind("<ButtonRelease-1>", lambda e: self.refresh_books_list())

    # Liste scrollable des livres
    def create_scrollable_books_list(self):
        list_container = ctk.CTkFrame(self, fg_color=COLOR_CONTENT)
        list_container.pack(fill="both", expand=True, padx=10, pady=10)
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color=COLOR_CONTENT,
            scrollbar_button_color="#888888",
            scrollbar_button_hover_color="#666666",
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=2, pady=2)

    # Lecture & affichage
    def refresh_books_list(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        session = get_session()
        try:
            books = session.query(Book).all()
            print(f"📊 Nombre de livres dans la DB: {len(books)}")

            search_text = self.search_entry.get().lower() if hasattr(self, "search_entry") else ""
            filter_available = self.availability_checkbox.get() == 1 if hasattr(self, "availability_checkbox") else False

            filtered = []
            for b in books:
                auteur = "N/A"
                if hasattr(b, "author") and b.author:
                    fn = getattr(b.author, "firstname", "") or ""
                    ln = getattr(b.author, "lastname", "") or ""
                    auteur = (f"{fn} {ln}".strip() or _label_for_author(b.author))
                editeur = "N/A"
                if hasattr(b, "publisher") and b.publisher:
                    editeur = getattr(b.publisher, "_name", "N/A")
                release_dt = getattr(b, "_release_date", None)

                item = {
                    "id": getattr(b, "_id", None),
                    "titre": getattr(b, "_title", "") or "",
                    "auteur": auteur,
                    "editeur": editeur,
                    "genre": getattr(b, "_genre", "") or "",
                    "pages": getattr(b, "_nb_pages", None),
                    "format": getattr(b, "_format", "") or "",
                    "release_date": release_dt.strftime("%Y-%m-%d") if release_dt else "",
                    "summary": getattr(b, "_summary", "") or "",
                    "image": getattr(b, "_image", None),
                    "status": getattr(b, "_status", "available"),
                    "author_id": getattr(b, "author_id", None),
                    "publisher_id": getattr(b, "publisher_id", None),
                }

                if search_text:
                    if (
                        search_text in str(item["id"]).lower()
                        or search_text in item["titre"].lower()
                        or search_text in item["auteur"].lower()
                        or search_text in item["editeur"].lower()
                        or search_text in item["genre"].lower()
                    ):
                        pass
                    else:
                        continue
                if filter_available and item["status"] != "available":
                    continue

                filtered.append(item)

            if not filtered:
                ctk.CTkLabel(self.scrollable_frame, text="Aucun livre trouvé",
                             font=("Arial", 14), text_color="#666666").pack(pady=50)
            else:
                for book in filtered:
                    self.add_book_card(book)

        except Exception as e:
            print(f"❌ Erreur lors du chargement des livres: {e}")
            import traceback; traceback.print_exc()
        finally:
            session.close()

    def add_book_card(self, book):
        card = ctk.CTkFrame(self.scrollable_frame, fg_color=COLOR_FORM, corner_radius=10)
        card.pack(fill="x", padx=10, pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", padx=15, pady=15)

        # Couverture (pictos placeholder)
        cover_frame = ctk.CTkFrame(inner, fg_color="white", width=80, height=120, corner_radius=5)
        cover_frame.pack(side="left", padx=(0, 20))
        cover_frame.pack_propagate(False)
        cover_icons = ["📕", "📘", "📗", "📙", "📓"]
        idx = (book["id"] or 0) % len(cover_icons)
        ctk.CTkLabel(cover_frame, text=cover_icons[idx], font=("Arial", 40)).pack(expand=True)

        # Infos
        info_frame = ctk.CTkFrame(inner, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(row, text="Titre :", font=("Arial", 13, "bold"), text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {book['titre']}", font=("Arial", 13, "bold"), text_color="#333333").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(row, text="Éditeur :", font=("Arial", 12, "bold"), text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {book['editeur']}", font=("Arial", 12), text_color="#333333").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x")
        ctk.CTkLabel(row, text="Auteur :", font=("Arial", 12, "bold"), text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {book['auteur']}", font=("Arial", 12), text_color="#333333").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row, text="Genre :", font=("Arial", 12, "bold"), text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {book.get('genre', 'N/A')}", font=("Arial", 12), text_color="#333333").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(0, 0))
        ctk.CTkLabel(row, text="Pages :", font=("Arial", 12, "bold"), text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {book.get('pages', '—') if book.get('pages') else '—'}",
                     font=("Arial", 12), text_color="#333333").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(0, 0))
        ctk.CTkLabel(row, text="Paru le :", font=("Arial", 12, "bold"), text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {book.get('release_date', '—') or '—'}",
                     font=("Arial", 12), text_color="#333333").pack(side="left")

        # Actions
        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.pack(side="right", padx=10)
        ctk.CTkButton(
            actions, text="✏️ Modifier", width=120, height=35,
            fg_color="#6366F1", hover_color="#4F46E5", font=("Arial", 11, "bold"),
            command=lambda b=book: self.open_edit_overlay(b)
        ).pack(pady=5)
        ctk.CTkButton(
            actions, text="🗑️ Supprimer", width=120, height=35,
            fg_color=PALE_RED, hover_color=PALE_RED_HOVER, font=("Arial", 11, "bold"),
            command=lambda b=book: self.delete_book(b["id"])
        ).pack(pady=5)

        status = book.get("status", "available")
        badge_text = "✓ Disponible" if status == "available" else f"⏳ {status}"
        badge_color = "green" if status == "available" else "#CC8B00"
        ctk.CTkLabel(actions, text=badge_text, font=("Arial", 10, "bold"),
                     text_color=badge_color).pack(pady=5)

    # ---------- CRUD ----------
    def open_create_overlay(self):
        BookOverlayWindow(self, on_validate=self.save_book).show()

    def open_edit_overlay(self, book):
        BookOverlayWindow(self, on_validate=self.save_book, book_data=book).show()

    def save_book(self, data, is_edit=False):
        session = get_session()
        try:
            # Vérifier existence auteur/éditeur
            author = session.query(Author).filter_by(_id=data["author_id"]).first()
            publisher = session.query(Publisher).filter_by(_id=data["publisher_id"]).first()
            if not author or not publisher:
                raise ValueError("Auteur ou Éditeur introuvable en DB.")

            if is_edit and data["id"] is not None:
                book = session.query(Book).filter_by(_id=data["id"]).first()
                if not book:
                    print(f"❌ Livre ID {data['id']} non trouvé")
                else:
                    book._title = data["titre"]
                    book._nb_pages = data["pages"]
                    book._genre = data["genre"]
                    book._summary = data["summary"]
                    book._format = data["format"]
                    book._release_date = data["release_date"]
                    book._image = data["image"]
                    book._status = data["status"]
                    book.author_id = data["author_id"]
                    book.publisher_id = data["publisher_id"]
                    session.commit()
                    print(f"✅ Livre modifié : {data['titre']} (ID: {data['id']})")
            else:
                new_book = Book(
                    _title=data["titre"],
                    _nb_pages=data["pages"],
                    _genre=data["genre"],
                    _summary=data["summary"],
                    _format=data["format"],
                    _release_date=data["release_date"],
                    _image=data["image"],
                    _status=data["status"],
                    author_id=data["author_id"],
                    publisher_id=data["publisher_id"],
                )
                session.add(new_book)
                session.commit()
                print(f"✅ Nouveau livre créé : {data['titre']} (ID: {getattr(new_book, '_id', '?')})")

            self.refresh_books_list()

        except Exception as e:
            session.rollback()
            print(f"❌ Erreur save_book : {e}")
            import traceback; traceback.print_exc()
        finally:
            session.close()

    def delete_book(self, book_id):
        session = get_session()
        try:
            book = session.query(Book).filter_by(_id=book_id).first()
            if book:
                title = getattr(book, "_title", "(sans titre)")
                session.delete(book)
                session.commit()
                print(f"✅ Livre supprimé : {title} (ID: {book_id})")
                self.refresh_books_list()
            else:
                print(f"❌ Livre ID {book_id} non trouvé")
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur delete_book : {e}")
            import traceback; traceback.print_exc()
        finally:
            session.close()

    # ---------- Navigation (alignée sur accueil.py) ----------
    def open_accueil(self):
        import subprocess
        if self._spawn_like_accueil("accueil.py"):
            self.after(1750, self.destroy)

    def open_livres(self):
        """Page courante → on ne relance pas la page."""
        self.hide_menu()

    def open_membres(self):
        import subprocess
        if self._spawn_like_accueil("client.py"):
            self.after(1750, self.destroy)

    def open_emprunts(self):
        import subprocess
        if self._spawn_like_accueil("emprunts.py"):
            self.after(1750, self.destroy)

    def open_employes(self):
        import subprocess
        if self._spawn_like_accueil("employes.py"):
            self.after(1750, self.destroy)

    def open_auteurs(self):
        import subprocess
        if self._spawn_like_accueil("auteurs.py"):
            self.after(1750, self.destroy)

    def open_editeurs(self):
        import subprocess
        if self._spawn_like_accueil("editeurs.py"):
            self.after(1750, self.destroy)

    # ---------- Menu hamburger (copie fonctionnelle de l’accueil) ----------
    def toggle_menu(self):
        if self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        if self.menu_frame is None:
            self.menu_frame = ctk.CTkFrame(self, fg_color="#FFB6C1", corner_radius=10, width=320, height=260)
        # Nettoyage
        for child in self.menu_frame.winfo_children():
            child.destroy()

        menu_buttons = [
            ("🏠 Accueil",   self.open_accueil),
            ("📚 Livres",    self.open_livres),     # courant
            ("👥 Membres",   self.open_membres),
            ("📖 Emprunts",  self.open_emprunts),
            ("💼 Employés",  self.open_employes),
            ("✍️ Auteurs",   self.open_auteurs),
            ("🏢 Éditeurs",  self.open_editeurs),
        ]

        for i, (text, command) in enumerate(menu_buttons):
            row = i // 2
            col = i % 2
            ctk.CTkButton(
                self.menu_frame, text=text, font=("Arial", 13, "bold"),
                fg_color="#D3D3D3", text_color="#666666",
                hover_color="#C0C0C0", height=60, corner_radius=8,
                command=command
            ).grid(row=row, column=col, padx=10, pady=10, sticky="ew")

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
