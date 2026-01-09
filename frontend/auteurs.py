import customtkinter as ctk
import sys
import os
from datetime import datetime, date
from PIL import Image
import subprocess

# === Init chemins & imports DB (comme accueil.py / client.py) ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from db.database import get_session

# -------- IMPORTS DES MODÈLES (ROBUSTES) --------
from Classes.base import Base
from Classes.person import Person
from Classes.customer import Customer  # ← IMPORTANT pour resoudre Borrow → Customer
from Classes.employee import Employee
from Classes.author import Author
from Classes.publisher import Publisher
from Classes.books import Book
from Classes.borrow import Borrow

# (Optionnel) forcer la configuration des mappers après tous les imports
from sqlalchemy.orm import configure_mappers
configure_mappers()

# Couleurs & style (cohérent)
PALE_GREEN = "#B5E6AB"
PALE_GREEN_HOVER = "#9FD695"
PALE_RED = "#FFBFBF"
PALE_RED_HOVER = "#FF9999"
COLOR_HEADER = "#FFB6C1"   # ← aligné sur accueil.py
COLOR_CONTENT = "#A8A8A8"
COLOR_FORM = "#D0D0D0"

# ---------- Helpers ----------
def _safe_str(v, default=""):
    return (str(v) if v is not None else default).strip()

def _initials(firstname: str, lastname: str) -> str:
    i1 = (firstname[:1] if firstname else "").upper()
    i2 = (lastname[:1] if lastname else "").upper()
    return (i1 + i2) or "A"

def _make_author_label(nick: str, fn: str, ln: str) -> str:
    """
    Construit un libellé lisible et non vide, même si certains champs manquent.
    Priorité : [Nick] Prénom Nom > Prénom Nom > Nick
    """
    fn = fn or ""
    ln = ln or ""
    nick = nick or ""
    if nick and (fn or ln):
        return f"[{nick}] {fn} {ln}".strip()
    if fn or ln:
        return f"{fn} {ln}".strip()
    return nick

def _author_to_dict(a: Author) -> dict:
    """Transforme un objet Author en dict d'affichage (robuste via getattr)."""
    d = {
        "id": getattr(a, "_id", None),
        "prenom": getattr(a, "firstname", "") or "",
        "nom": getattr(a, "lastname", "") or "",
        "birthdate": "",
        "nickname": getattr(a, "_nickName", "") or "",
        "nb_books": 0,
    }
    bd = getattr(a, "birthdate", None)
    d["birthdate"] = bd.strftime("%Y-%m-%d") if bd else ""
    try:
        d["nb_books"] = len(getattr(a, "books", []) or [])
    except Exception:
        d["nb_books"] = 0
    return d


# ---------- Popup création / modification d'un auteur ----------
class AuthorOverlayWindow:
    """
    Popup scrollable "Ajouter / Modifier un auteur"
    Champs respectant la classe Author:
    - firstname, lastname, birthdate (hérités de Person)
    - _nickName (String(50), REQUIRED)
    """
    def __init__(self, parent, on_validate=None, author_data=None):
        self.parent = parent
        self.on_validate = on_validate
        self.author_data = author_data or {}
        self.is_edit = author_data is not None

    # === NAVIGATION (alignée sur accueil.py : NO withdraw, délai ~1750 ms) ===
    def _spawn_like_accueil(self, script_path: str):
        if not os.path.exists(script_path):
            print(f"❌ Fichier non trouvé: {script_path}")
            return False
        try:
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, script_path],
                                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                subprocess.Popen([sys.executable, script_path])  # pas de start_new_session
            return True
        except Exception as e:
            print(f"❌ Erreur lancement {script_path}: {e}")
            import traceback; traceback.print_exc()
            return False

    def open_livres(self):
        print("📚 Ouverture de la gestion des livres...")
        if self._spawn_like_accueil(os.path.join(current_dir, "liste_de_livre.py")):
            self.win.after(1750, self.win.destroy)

    def open_membres(self):
        print("📂 Ouverture de la gestion des membres...")
        if self._spawn_like_accueil(os.path.join(current_dir, "client.py")):
            self.win.after(1750, self.win.destroy)

    def open_emprunts(self):
        print("📖 Ouverture de la gestion des emprunts...")
        if self._spawn_like_accueil(os.path.join(current_dir, "emprunts.py")):
            self.win.after(1750, self.win.destroy)

    def open_employes(self):
        print("💼 Ouverture de la gestion des employés...")
        if self._spawn_like_accueil(os.path.join(current_dir, "employes.py")):
            self.win.after(1750, self.win.destroy)

    def open_auteurs(self):
        """Déjà sur la page auteurs → fermer la popup."""
        try:
            self.win.destroy()
        except Exception:
            pass

    def open_editeurs(self):
        print("🏢 Ouverture de la gestion des éditeurs...")
        if self._spawn_like_accueil(os.path.join(current_dir, "editeurs.py")):
            self.win.after(1750, self.win.destroy)

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.title("Modifier un auteur" if self.is_edit else "Ajouter un auteur")
        self.win.geometry("980x720")
        self.win.minsize(820, 560)
        self.win.resizable(True, True)

        # Header (popup)
        fr_header = ctk.CTkFrame(self.win, fg_color=COLOR_HEADER, corner_radius=15, height=80)
        fr_header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(fr_header, text=self.win.title(), font=("Arial", 24, "bold")).pack(pady=25)

        # Content
        fr_content = ctk.CTkFrame(self.win, fg_color=COLOR_CONTENT, corner_radius=15)
        fr_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Form container (GRID pour garder la barre de boutons visible)
        fr_form = ctk.CTkFrame(fr_content, fg_color=COLOR_FORM, corner_radius=15)
        fr_form.pack(fill="both", expand=True, padx=40, pady=40)

        # Configuration du layout en grille
        fr_form.grid_rowconfigure(0, weight=1)   # zone scrollable prend l'espace
        fr_form.grid_rowconfigure(1, weight=0)   # barre de boutons fixe
        fr_form.grid_columnconfigure(0, weight=1)

        # Zone scrollable (ligne 0)
        fr_scroll = ctk.CTkScrollableFrame(
            fr_form, fg_color=COLOR_FORM, corner_radius=0,
            scrollbar_button_color="#888888", scrollbar_button_hover_color="#666666",
            width=820, height=480
        )
        fr_scroll.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 12))

        fr_fields = ctk.CTkFrame(fr_scroll, fg_color=COLOR_FORM)
        fr_fields.pack(fill="x", expand=False, padx=20, pady=20)

        row = 0
        # ID (lecture seule si édition)
        ctk.CTkLabel(fr_fields, text="ID :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=10
        )
        self.entry_id = ctk.CTkEntry(fr_fields, width=220, height=40, font=("Arial", 12))
        self.entry_id.grid(row=row, column=1, padx=20, pady=10, sticky="w")
        if self.is_edit:
            self.entry_id.insert(0, str(self.author_data.get("id", "")))
            self.entry_id.configure(state="disabled")
        row += 1

        # Prénom
        ctk.CTkLabel(fr_fields, text="PRÉNOM :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_prenom = ctk.CTkEntry(fr_fields, width=340, height=40, font=("Arial", 12))
        self.entry_prenom.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Nom
        ctk.CTkLabel(fr_fields, text="NOM :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_nom = ctk.CTkEntry(fr_fields, width=340, height=40, font=("Arial", 12))
        self.entry_nom.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Date de naissance
        ctk.CTkLabel(fr_fields, text="DATE DE NAISSANCE (YYYY-MM-DD) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_birthdate = ctk.CTkEntry(fr_fields, width=220, height=40, font=("Arial", 12))
        self.entry_birthdate.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Pseudonyme (≤50)
        ctk.CTkLabel(fr_fields, text="PSEUDONYME (≤50) :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_nick = ctk.CTkEntry(fr_fields, width=340, height=40, font=("Arial", 12))
        self.entry_nick.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Pré-remplissage si édition
        if self.is_edit:
            self.entry_prenom.insert(0, self.author_data.get("prenom", ""))
            self.entry_nom.insert(0, self.author_data.get("nom", ""))
            self.entry_birthdate.insert(0, self.author_data.get("birthdate", ""))
            self.entry_nick.insert(0, self.author_data.get("nickname", ""))

        # Barre de boutons (ligne 1) — TOUJOURS VISIBLE
        fr_buttons = ctk.CTkFrame(fr_form, fg_color=COLOR_FORM)
        fr_buttons.grid(row=1, column=0, sticky="ew", padx=20, pady=(4, 14))

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

        # Topmost court
        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.focus_force()
        self.win.after(120, lambda: self.win.attributes("-topmost", False))

    def _show_error(self, message: str):
        err = ctk.CTkToplevel(self.parent)
        err.title("Erreur")
        err.geometry("460x160")
        ctk.CTkLabel(err, text=message, font=("Arial", 13, "bold")).pack(pady=40)
        ctk.CTkButton(err, text="OK", command=err.destroy, width=100).pack()

    def validate(self):
        # Collecte
        data = {
            "id": self.author_data.get("id") if self.is_edit else None,
            "prenom": self.entry_prenom.get().strip(),
            "nom": self.entry_nom.get().strip(),
            "birthdate": self.entry_birthdate.get().strip(),
            "nickname": self.entry_nick.get().strip(),
        }
        # Requis
        if not data["prenom"] or not data["nom"] or not data["birthdate"] or not data["nickname"]:
            self._show_error("❌ Tous les champs sont obligatoires.")
            return
        if len(data["nickname"]) > 50:
            self._show_error("❌ Le pseudonyme doit faire au plus 50 caractères.")
            return
        # Date
        try:
            bd = datetime.strptime(data["birthdate"], "%Y-%m-%d").date()
        except Exception:
            self._show_error("❌ La date de naissance doit être au format YYYY-MM-DD.")
            return
        if bd > date.today():
            self._show_error("❌ La date de naissance ne peut pas être dans le futur.")
            return
        data["birthdate"] = bd

        # Callback (save DB)
        if self.on_validate:
            self.on_validate(data, is_edit=self.is_edit)
        self.win.destroy()


# ---------- Popup détails auteur (lecture seule) ----------
class AuthorDetailsOverlay:
    def __init__(self, parent, author_dict: dict):
        self.parent = parent
        self.author_dict = author_dict or {}

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.title(f"Détails Auteur #{self.author_dict.get('id', '')}")
        self.win.geometry("900x600")
        self.win.minsize(760, 520)
        self.win.resizable(True, True)

        fr_header = ctk.CTkFrame(self.win, fg_color=COLOR_HEADER, corner_radius=15, height=80)
        fr_header.pack(fill="x", padx=20, pady=20)
        title = f"{self.author_dict.get('prenom','')} {self.author_dict.get('nom','')}".strip() or "Auteur"
        nick = self.author_dict.get("nickname", "")
        display = f"{title} [{nick}]" if nick else title
        ctk.CTkLabel(fr_header, text=f"Détails — {display}", font=("Arial", 24, "bold")).pack(pady=25)

        fr_content = ctk.CTkFrame(self.win, fg_color=COLOR_CONTENT, corner_radius=15)
        fr_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        fr_form = ctk.CTkFrame(fr_content, fg_color=COLOR_FORM, corner_radius=15)
        fr_form.pack(fill="both", expand=True, padx=40, pady=40)

        fr_scroll = ctk.CTkScrollableFrame(
            fr_form, fg_color=COLOR_FORM, corner_radius=0,
            scrollbar_button_color="#888888", scrollbar_button_hover_color="#666666",
            width=780, height=420
        )
        fr_scroll.pack(side="top", fill="both", expand=True, padx=0, pady=(0, 12))

        fields = [
            ("ID", _safe_str(self.author_dict.get("id"))),
            ("Prénom", _safe_str(self.author_dict.get("prenom"))),
            ("Nom", _safe_str(self.author_dict.get("nom"))),
            ("Date de naissance", _safe_str(self.author_dict.get("birthdate"))),
            ("Pseudonyme", _safe_str(self.author_dict.get("nickname"))),
            ("Livres associés", _safe_str(self.author_dict.get("nb_books"))),
        ]

        fr_fields = ctk.CTkFrame(fr_scroll, fg_color=COLOR_FORM)
        fr_fields.pack(fill="x", expand=False, padx=20, pady=20)
        for i, (label, value) in enumerate(fields):
            row = ctk.CTkFrame(fr_fields, fg_color="transparent")
            row.pack(fill="x", pady=6)
            ctk.CTkLabel(row, text=f"{label} :", font=("Arial", 14, "bold")).pack(side="left")
            ctk.CTkLabel(row, text=f" {value}", font=("Arial", 14)).pack(side="left")

        fr_buttons = ctk.CTkFrame(fr_form, fg_color=COLOR_FORM)
        fr_buttons.pack(side="bottom", fill="x", padx=20, pady=(4, 14))
        ctk.CTkButton(
            fr_buttons, text="FERMER",
            fg_color=PALE_GREEN, hover_color=PALE_GREEN_HOVER,
            width=180, height=50, font=("Arial", 14, "bold"),
            command=self.win.destroy
        ).pack(side="right", padx=10)

        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.focus_force()
        self.win.after(120, lambda: self.win.attributes("-topmost", False))


# ---------- Fenêtre principale ----------
class AuthorsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion Auteurs")
        self.geometry("1100x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.create_header()
        self.create_toolbar()
        self.create_search_bar()
        self.create_scrollable_authors_list()
        self.refresh_authors_list()

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

    # ---------- Header aligné sur accueil.py ----------
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

    # ---------- Toolbar ----------
    def create_toolbar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=50, pady=(5, 0))
        ctk.CTkButton(
            bar, text="➕ AJOUTER AUTEUR", fg_color="#6366F1", hover_color="#4F46E5",
            height=42, font=("Arial", 13, "bold"),
            command=self.open_create_overlay
        ).pack(side="right")

    # ---------- Search ----------
    def create_search_bar(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=50, pady=10)
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Rechercher par ID, NOM, PRÉNOM, PSEUDONYME",
            height=40, font=("Arial", 12)
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_authors_list())

    # ---------- Liste d'auteurs ----------
    def create_scrollable_authors_list(self):
        self.authors_scrollable_frame = ctk.CTkScrollableFrame(
            self, fg_color="#E8E8E8", corner_radius=10
        )
        self.authors_scrollable_frame.pack(fill="both", expand=True, padx=50, pady=(10, 20))

    # ---------- Navigation (fenêtre principale) ----------
    def open_accueil(self):
        if self._spawn_like_accueil("accueil.py"):
            self.after(1750, self.destroy)

    def open_livres(self):
        if self._spawn_like_accueil("liste_de_livre.py"):
            self.after(1750, self.destroy)

    def open_membres(self):
        if self._spawn_like_accueil("client.py"):
            self.after(1750, self.destroy)

    def open_employes(self):
        if self._spawn_like_accueil("employes.py"):
            self.after(1750, self.destroy)

    def open_emprunts(self):
        if self._spawn_like_accueil("emprunts.py"):
            self.after(1750, self.destroy)

    def open_editeurs(self):
        if self._spawn_like_accueil("editeurs.py"):
            self.after(1750, self.destroy)

    def open_auteurs(self):
        """Déjà sur la page auteurs → juste masquer le menu."""
        self.hide_menu()

    # ---------- Menu hamburger (aligné accueil.py) ----------
    def toggle_menu(self):
        if self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        if self.menu_frame is None:
            self.menu_frame = ctk.CTkFrame(self, fg_color="#FFB6C1",
                                           corner_radius=10, width=320, height=260)
        # Nettoyage (si recréé)
        for child in self.menu_frame.winfo_children():
            child.destroy()

        menu_buttons = [
            ("🏠 Accueil",   self.open_accueil),
            ("📚 Livres",    self.open_livres),
            ("👥 Membres",   self.open_membres),
            ("📖 Emprunts",  self.open_emprunts),
            ("💼 Employés",  self.open_employes),
            ("✍️ Auteurs",   self.open_auteurs),   # ← page courante
            ("🏢 Éditeurs",  self.open_editeurs),
        ]

        for i, (text, command) in enumerate(menu_buttons):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                self.menu_frame, text=text, font=("Arial", 13, "bold"),
                fg_color="#D3D3D3", text_color="#666666",
                hover_color="#C0C0C0", height=60, corner_radius=8,
                command=command
            )
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

    # ---------- DATA ----------
    def refresh_authors_list(self):
        # Clear
        for w in self.authors_scrollable_frame.winfo_children():
            w.destroy()

        session = get_session()
        try:
            # Chargement “léger” : colonnes locales uniquement
            rows = session.query(
                Author._id, Author._nickName, Author.firstname, Author.lastname, Author.birthdate
            ).order_by(Author._id.asc()).all()
            print(f"📊 Auteurs trouvés: {len(rows)}")

            search = self.search_entry.get().lower() if hasattr(self, "search_entry") else ""
            prepared = []
            for _id, nick, fn, ln, bd in rows:
                label = _make_author_label(nick, fn, ln)
                birth_txt = bd.strftime("%Y-%m-%d") if bd else ""
                item = {
                    "id": _id,
                    "prenom": fn or "",
                    "nom": ln or "",
                    "birthdate": birth_txt,
                    "nickname": nick or "",
                }
                # Compter les livres liés (tolérant aux erreurs)
                try:
                    a = session.query(Author).filter(Author._id == _id).first()
                    item["nb_books"] = len(getattr(a, "books", []) or []) if a else 0
                except Exception:
                    item["nb_books"] = 0

                # Filtrage
                if search:
                    if (
                        search in str(item["id"]).lower()
                        or search in (item["nom"] or "").lower()
                        or search in (item["prenom"] or "").lower()
                        or search in (item["nickname"] or "").lower()
                        or search in label.lower()
                    ):
                        prepared.append(item)
                else:
                    prepared.append(item)

            if not prepared:
                ctk.CTkLabel(
                    self.authors_scrollable_frame, text="Aucun auteur trouvé",
                    font=("Arial", 14), text_color="#666666"
                ).pack(pady=50)
            else:
                for item in prepared:
                    self.create_author_card(item)

        except Exception as e:
            print(f"❌ Erreur lors du chargement des auteurs: {e}")
            import traceback
            traceback.print_exc()
            ctk.CTkLabel(
                self.authors_scrollable_frame, text="Erreur de chargement.",
                font=("Arial", 14), text_color="red"
            ).pack(pady=50)
        finally:
            session.close()

    def create_author_card(self, au: dict):
        card_frame = ctk.CTkFrame(
            self.authors_scrollable_frame, fg_color="#F5F5F5",
            corner_radius=10, border_width=2, border_color="#D0D0D0"
        )
        card_frame.pack(fill="x", padx=15, pady=8)

        inner = ctk.CTkFrame(card_frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=15)

        # Avatar
        avatar_frame = ctk.CTkFrame(inner, fg_color="#6366F1", width=100, height=100, corner_radius=50)
        avatar_frame.pack(side="left", padx=(0, 20))
        avatar_frame.pack_propagate(False)
        initials = _initials(au.get("prenom",""), au.get("nom",""))
        ctk.CTkLabel(avatar_frame, text=initials, font=("Arial", 32, "bold"), text_color="white").pack(expand=True)

        # Infos
        info_frame = ctk.CTkFrame(inner, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # Nom + pseudo
        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(0, 6))
        full_name = f"{au.get('prenom','')} {au.get('nom','')}".strip()
        ctk.CTkLabel(row, text=full_name or "Auteur (sans nom)", font=("Arial", 14, "bold"),
                     text_color="#333333").pack(side="left")
        if au.get("nickname"):
            ctk.CTkLabel(row, text=f" [{au['nickname']}]", font=("Arial", 14, "bold"),
                         text_color="#7C3AED").pack(side="left")

        if au.get("birthdate"):
            row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(2, 2))
            ctk.CTkLabel(row, text="Naissance :", font=("Arial", 12, "bold"),
                         text_color="#555555").pack(side="left")
            ctk.CTkLabel(row, text=f" {au['birthdate']}", font=("Arial", 12),
                         text_color="#333333").pack(side="left")

        # ID + nb livres
        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(2, 0))
        ctk.CTkLabel(row, text="ID Auteur :", font=("Arial", 12, "bold"),
                     text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" #{au.get('id','')}", font=("Arial", 12),
                     text_color="#666666").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(2, 0))
        ctk.CTkLabel(row, text="Livres associés :", font=("Arial", 12, "bold"),
                     text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {au.get('nb_books',0)}", font=("Arial", 12),
                     text_color="#333333").pack(side="left")

        # Actions
        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.pack(side="right", padx=10)
        ctk.CTkButton(
            actions, text="ℹ️ Détails", width=120, height=35,
            fg_color="#6366F1", hover_color="#4F46E5", font=("Arial", 11, "bold"),
            command=lambda d=au: AuthorDetailsOverlay(self, d).show()
        ).pack(pady=5)
        ctk.CTkButton(
            actions, text="✏️ Modifier", width=120, height=35,
            fg_color="#6366F1", hover_color="#4F46E5", font=("Arial", 11, "bold"),
            command=lambda d=au: self.open_edit_overlay(d)
        ).pack(pady=5)
        ctk.CTkButton(
            actions, text="🗑️ Supprimer", width=120, height=35,
            fg_color=PALE_RED, hover_color=PALE_RED_HOVER, font=("Arial", 11, "bold"),
            command=lambda d=au: self.delete_author(d["id"])
        ).pack(pady=5)

    # ---------- CRUD ----------
    def open_create_overlay(self):
        AuthorOverlayWindow(self, on_validate=self.save_author).show()

    def open_edit_overlay(self, au_dict: dict):
        AuthorOverlayWindow(self, on_validate=self.save_author, author_data=au_dict).show()

    def save_author(self, data, is_edit=False):
        """
        Insert / Update Author en base.
        Respecte la structure de la classe Author (_nickName) + Person (firstname, lastname, birthdate).
        """
        session = get_session()
        try:
            # Anti-doublon simple (optionnel)
            existing = session.query(Author).filter(
                Author.firstname == data["prenom"],
                Author.lastname == data["nom"],
                Author.birthdate == data["birthdate"],
                Author._nickName == data["nickname"]
            ).first()
            if existing and (not is_edit or existing._id != data["id"]):
                self._toast_error("Un auteur identique existe déjà.")
                return

            if is_edit and data["id"] is not None:
                au = session.query(Author).filter_by(_id=data["id"]).first()
                if not au:
                    self._toast_error(f"Auteur ID {data['id']} introuvable.")
                    return
                au.firstname = data["prenom"]
                au.lastname = data["nom"]
                au.birthdate = data["birthdate"]
                au._nickName = data["nickname"]
                session.commit()
                print(f"✅ Auteur modifié : {au.firstname} {au.lastname} (ID: {au._id})")
            else:
                new_au = Author(
                    firstname=data["prenom"],
                    lastname=data["nom"],
                    birthdate=data["birthdate"],
                    _nickName=data["nickname"],
                )
                session.add(new_au)
                session.commit()
                print(f"✅ Nouvel auteur créé : {new_au.firstname} {new_au.lastname} (ID: {new_au._id})")

            self.refresh_authors_list()

        except Exception as e:
            session.rollback()
            print(f"❌ Erreur save_author : {e}")
            import traceback
            traceback.print_exc()
            self._toast_error("Erreur lors de l’enregistrement.")
        finally:
            session.close()

    def delete_author(self, au_id: int):
        session = get_session()
        try:
            au = session.query(Author).filter_by(_id=au_id).first()
            if not au:
                self._toast_error("Auteur introuvable.")
                return

            # Empêcher la suppression si des livres y sont liés
            nb = len(getattr(au, "books", []) or [])
            if nb > 0:
                self._toast_error(f"Impossible de supprimer : {nb} livre(s) associé(s).")
                return

            fullname = f"{au.firstname} {au.lastname}"
            session.delete(au)
            session.commit()
            print(f"✅ Auteur supprimé : {fullname} (ID: {au_id})")
            self.refresh_authors_list()

        except Exception as e:
            session.rollback()
            print(f"❌ Erreur delete_author : {e}")
            import traceback
            traceback.print_exc()
            self._toast_error("Erreur lors de la suppression.")
        finally:
            session.close()

    # Toast simple
    def _toast_error(self, msg: str):
        win = ctk.CTkToplevel(self)
        win.title("Erreur")
        win.geometry("420x140")
        ctk.CTkLabel(win, text=msg, font=("Arial", 13, "bold")).pack(pady=30)
        ctk.CTkButton(win, text="OK", command=win.destroy, width=100,
                      fg_color=PALE_RED, hover_color=PALE_RED_HOVER).pack()



app = AuthorsApp()
app.mainloop()
