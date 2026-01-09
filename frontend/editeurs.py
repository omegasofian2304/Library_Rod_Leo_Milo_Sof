import customtkinter as ctk
import sys
import os
from PIL import Image
import subprocess
from datetime import datetime  # prêt si tu ajoutes d'autres champs

# === Init chemins & imports DB (comme accueil.py) ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from db.database import get_session

# -------- IMPORTS DES MODÈLES --------
from Classes.base import Base
# Ces imports complets garantissent les relations (comme sur accueil.py)
from Classes.person import Person
from Classes.customer import Customer
from Classes.employee import Employee
from Classes.author import Author
from Classes.publisher import Publisher
from Classes.books import Book
from Classes.borrow import Borrow

# (Optionnel) forcer la configuration des mappers après tous les imports
from sqlalchemy.orm import configure_mappers
configure_mappers()

# Couleurs & style (identiques à accueil)
PALE_GREEN = "#B5E6AB"
PALE_GREEN_HOVER = "#9FD695"
PALE_RED = "#FFBFBF"
PALE_RED_HOVER = "#FF9999"
COLOR_HEADER = "#FFB6C1"   # ← même que accueil.py
COLOR_CONTENT = "#A8A8A8"
COLOR_FORM = "#D0D0D0"

# ---------- Helpers ----------
def _safe_str(v, default=""):
    return (str(v) if v is not None else default).strip()

def _initials_from_name(name: str) -> str:
    s = (name or "").strip()
    if not s:
        return "É"  # initiale par défaut
    s = s.replace("-", " ").replace("_", " ")
    parts = [p for p in s.split() if p]
    if not parts:
        return (s[:2] or "É").upper()
    if len(parts[0]) >= 2:
        return parts[0][:2].upper()
    if len(parts) > 1:
        return (parts[0] + parts[1][:1]).upper()
    return parts[0].upper()

def _publisher_to_dict(pu: Publisher) -> dict:
    """Transforme un Publisher en dict d'affichage (robuste via getattr)."""
    d = {
        "id": getattr(pu, "_id", None),
        "name": getattr(pu, "_name", "") or "",
        "nb_books": 0,
    }
    try:
        d["nb_books"] = len(getattr(pu, "books", []) or [])
    except Exception:
        d["nb_books"] = 0
    return d


# ---------- Popup création / modification d'un éditeur ----------
class PublisherOverlayWindow:
    """
    Popup scrollable "Ajouter / Modifier un éditeur"
    Champs respectant la classe Publisher:
    - _name (String, REQUIRED)
    """
    def __init__(self, parent, on_validate=None, publisher_data=None):
        self.parent = parent
        self.on_validate = on_validate
        self.publisher_data = publisher_data or {}
        self.is_edit = publisher_data is not None

    # === NAVIGATION (même pattern que accueil.py : NO withdraw, délai ~1750 ms) ===
    def _spawn_like_accueil(self, script_path: str):
        if not os.path.exists(script_path):
            print(f"❌ Fichier non trouvé: {script_path}")
            return False
        try:
            if sys.platform == "win32":
                # OK sous Windows, ne change pas l'UX par rapport à accueil
                subprocess.Popen([sys.executable, script_path],
                                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                # Alignement strict sur accueil.py: PAS de start_new_session ici
                subprocess.Popen([sys.executable, script_path])
            return True
        except Exception as e:
            print(f"❌ Erreur lancement {script_path}: {e}")
            import traceback; traceback.print_exc()
            return False

    def open_livres(self):
        if self._spawn_like_accueil(os.path.join(current_dir, "liste_de_livre.py")):
            # Pas de withdraw, délai identique à accueil
            self.win.after(1750, self.win.destroy)

    def open_membres(self):
        if self._spawn_like_accueil(os.path.join(current_dir, "client.py")):
            self.win.after(1750, self.win.destroy)

    def open_emprunts(self):
        if self._spawn_like_accueil(os.path.join(current_dir, "emprunts.py")):
            self.win.after(1750, self.win.destroy)

    def open_employes(self):
        if self._spawn_like_accueil(os.path.join(current_dir, "employes.py")):
            self.win.after(1750, self.win.destroy)

    def open_auteurs(self):
        if self._spawn_like_accueil(os.path.join(current_dir, "auteurs.py")):
            self.win.after(1750, self.win.destroy)

    def open_accueil(self):
        if self._spawn_like_accueil(os.path.join(current_dir, "accueil.py")):
            self.win.after(1750, self.win.destroy)

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.title("Modifier un éditeur" if self.is_edit else "Ajouter un éditeur")
        self.win.geometry("880x600")
        self.win.minsize(740, 520)
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

        # Grid layout
        fr_form.grid_rowconfigure(0, weight=1)   # scrollable
        fr_form.grid_rowconfigure(1, weight=0)   # boutons fixes
        fr_form.grid_columnconfigure(0, weight=1)

        # Zone scrollable (ligne 0)
        fr_scroll = ctk.CTkScrollableFrame(
            fr_form, fg_color=COLOR_FORM, corner_radius=0,
            scrollbar_button_color="#888888", scrollbar_button_hover_color="#666666",
            width=760, height=380
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
            self.entry_id.insert(0, str(self.publisher_data.get("id", "")))
            self.entry_id.configure(state="disabled")
        row += 1

        # Nom éditeur (REQUIRED)
        ctk.CTkLabel(fr_fields, text="NOM DE L’ÉDITEUR :", font=("Arial", 14, "bold")).grid(
            row=row, column=0, sticky="w", padx=20, pady=8
        )
        self.entry_name = ctk.CTkEntry(fr_fields, width=420, height=40, font=("Arial", 12))
        self.entry_name.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Pré-remplissage si édition
        if self.is_edit:
            self.entry_name.insert(0, self.publisher_data.get("name", ""))

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
            "id": self.publisher_data.get("id") if self.is_edit else None,
            "name": self.entry_name.get().strip(),
        }
        # Requis
        if not data["name"]:
            self._show_error("❌ Le nom de l’éditeur est obligatoire.")
            return
        if len(data["name"]) > 100:
            self._show_error("❌ Le nom de l’éditeur doit faire au plus 100 caractères.")
            return

        # Callback (save DB)
        if self.on_validate:
            self.on_validate(data, is_edit=self.is_edit)
        self.win.destroy()


# ---------- Popup détails éditeur (lecture seule) ----------
class PublisherDetailsOverlay:
    def __init__(self, parent, publisher_dict: dict):
        self.parent = parent
        self.publisher_dict = publisher_dict or {}

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.title(f"Détails Éditeur #{self.publisher_dict.get('id', '')}")
        self.win.geometry("820x520")
        self.win.minsize(720, 460)
        self.win.resizable(True, True)

        fr_header = ctk.CTkFrame(self.win, fg_color=COLOR_HEADER, corner_radius=15, height=80)
        fr_header.pack(fill="x", padx=20, pady=20)
        title = self.publisher_dict.get("name", "").strip() or "Éditeur"
        ctk.CTkLabel(fr_header, text=f"Détails — {title}", font=("Arial", 24, "bold")).pack(pady=25)

        fr_content = ctk.CTkFrame(self.win, fg_color=COLOR_CONTENT, corner_radius=15)
        fr_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        fr_form = ctk.CTkFrame(fr_content, fg_color=COLOR_FORM, corner_radius=15)
        fr_form.pack(fill="both", expand=True, padx=40, pady=40)

        fr_scroll = ctk.CTkScrollableFrame(
            fr_form, fg_color=COLOR_FORM, corner_radius=0,
            scrollbar_button_color="#888888", scrollbar_button_hover_color="#666666",
            width=720, height=360
        )
        fr_scroll.pack(side="top", fill="both", expand=True, padx=0, pady=(0, 12))

        fields = [
            ("ID", _safe_str(self.publisher_dict.get("id"))),
            ("Nom", _safe_str(self.publisher_dict.get("name"))),
            ("Livres associés", _safe_str(self.publisher_dict.get("nb_books"))),
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
class EditeursApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion Éditeurs")
        self.geometry("1100x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.create_header()
        self.create_toolbar()
        self.create_search_bar()
        self.create_scrollable_publishers_list()
        self.refresh_publishers_list()

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

    # ---------- Header (identique à accueil.py) ----------
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

        # Menu hamburger (même style que accueil.py)
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
            bar, text="➕ AJOUTER ÉDITEUR", fg_color="#6366F1", hover_color="#4F46E5",
            height=42, font=("Arial", 13, "bold"),
            command=self.open_create_overlay
        ).pack(side="right")

    # ---------- Search ----------
    def create_search_bar(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=50, pady=10)
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Rechercher par ID, NOM",
            height=40, font=("Arial", 12)
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_publishers_list())

    # ---------- Liste d'éditeurs ----------
    def create_scrollable_publishers_list(self):
        self.publishers_scrollable_frame = ctk.CTkScrollableFrame(
            self, fg_color="#E8E8E8", corner_radius=10
        )
        self.publishers_scrollable_frame.pack(fill="both", expand=True, padx=50, pady=(10, 20))

    # ---------- Navigation (même structure que accueil) ----------
    def open_accueil(self):
        if self._spawn_like_accueil("accueil.py"):
            self.after(1750, self.destroy)

    def open_livres(self):
        if self._spawn_like_accueil("liste_de_livre.py"):
            self.after(1750, self.destroy)

    def open_membres(self):
        if self._spawn_like_accueil("client.py"):
            self.after(1750, self.destroy)

    def open_emprunts(self):
        if self._spawn_like_accueil("emprunts.py"):
            self.after(1750, self.destroy)

    def open_employes(self):
        if self._spawn_like_accueil("employes.py"):
            self.after(1750, self.destroy)

    def open_auteurs(self):
        if self._spawn_like_accueil("auteurs.py"):
            self.after(1750, self.destroy)

    def open_editeurs(self):
        """Déjà sur la page éditeurs → comme sur accueil, on ne relance pas la page courante."""
        self.hide_menu()

    # ---------- Menu hamburger (copie fonctionnelle de l’accueil) ----------
    def toggle_menu(self):
        if self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        if self.menu_frame is None:
            self.menu_frame = ctk.CTkFrame(self, fg_color="#FFB6C1",
                                           corner_radius=10, width=320, height=260)
        # Nettoyage
        for child in self.menu_frame.winfo_children():
            child.destroy()

        menu_buttons = [
            ("🏠 Accueil",   self.open_accueil),
            ("📚 Livres",    self.open_livres),
            ("👥 Membres",   self.open_membres),
            ("📖 Emprunts",  self.open_emprunts),
            ("💼 Employés",  self.open_employes),
            ("✍️ Auteurs",   self.open_auteurs),
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
    def refresh_publishers_list(self):
        # Clear
        for w in self.publishers_scrollable_frame.winfo_children():
            w.destroy()

        session = get_session()
        try:
            # Chargement léger : colonnes locales
            rows = session.query(
                Publisher._id, Publisher._name
            ).order_by(Publisher._id.asc()).all()
            print(f"🏢 Éditeurs trouvés: {len(rows)}")

            search = self.search_entry.get().lower() if hasattr(self, "search_entry") else ""
            prepared = []
            for _id, name in rows:
                item = {
                    "id": _id,
                    "name": name or "",
                }
                # Compter les livres liés (tolérant aux erreurs)
                try:
                    pu = session.query(Publisher).filter(Publisher._id == _id).first()
                    item["nb_books"] = len(getattr(pu, "books", []) or []) if pu else 0
                except Exception:
                    item["nb_books"] = 0

                # Filtrage
                if search:
                    if (
                        search in str(item["id"]).lower()
                        or search in (item["name"] or "").lower()
                    ):
                        prepared.append(item)
                else:
                    prepared.append(item)

            if not prepared:
                ctk.CTkLabel(
                    self.publishers_scrollable_frame, text="Aucun éditeur trouvé",
                    font=("Arial", 14), text_color="#666666"
                ).pack(pady=50)
            else:
                for item in prepared:
                    self.create_publisher_card(item)

        except Exception as e:
            print(f"❌ Erreur lors du chargement des éditeurs: {e}")
            import traceback; traceback.print_exc()
            ctk.CTkLabel(
                self.publishers_scrollable_frame, text="Erreur de chargement.",
                font=("Arial", 14), text_color="red"
            ).pack(pady=50)
        finally:
            session.close()

    def create_publisher_card(self, pu: dict):
        card_frame = ctk.CTkFrame(
            self.publishers_scrollable_frame, fg_color="#F5F5F5",
            corner_radius=10, border_width=2, border_color="#D0D0D0"
        )
        card_frame.pack(fill="x", padx=15, pady=8)

        inner = ctk.CTkFrame(card_frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=15)

        # Avatar
        avatar_frame = ctk.CTkFrame(inner, fg_color="#6366F1", width=100, height=100, corner_radius=50)
        avatar_frame.pack(side="left", padx=(0, 20))
        avatar_frame.pack_propagate(False)
        initials = _initials_from_name(pu.get("name", ""))
        ctk.CTkLabel(avatar_frame, text=initials, font=("Arial", 32, "bold"), text_color="white").pack(expand=True)

        # Infos
        info_frame = ctk.CTkFrame(inner, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # Nom éditeur
        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(row, text=pu.get("name","") or "Éditeur (sans nom)", font=("Arial", 14, "bold"),
                     text_color="#333333").pack(side="left")

        # ID + nb livres
        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(2, 0))
        ctk.CTkLabel(row, text="ID Éditeur :", font=("Arial", 12, "bold"),
                     text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" #{pu.get('id','')}", font=("Arial", 12),
                     text_color="#666666").pack(side="left")

        row = ctk.CTkFrame(info_frame, fg_color="transparent"); row.pack(fill="x", pady=(2, 0))
        ctk.CTkLabel(row, text="Livres associés :", font=("Arial", 12, "bold"),
                     text_color="#555555").pack(side="left")
        ctk.CTkLabel(row, text=f" {pu.get('nb_books',0)}", font=("Arial", 12),
                     text_color="#333333").pack(side="left")

        # Actions
        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.pack(side="right", padx=10)
        ctk.CTkButton(
            actions, text="ℹ️ Détails", width=120, height=35,
            fg_color="#6366F1", hover_color="#4F46E5", font=("Arial", 11, "bold"),
            command=lambda d=pu: PublisherDetailsOverlay(self, d).show()
        ).pack(pady=5)
        ctk.CTkButton(
            actions, text="✏️ Modifier", width=120, height=35,
            fg_color="#6366F1", hover_color="#4F46E5", font=("Arial", 11, "bold"),
            command=lambda d=pu: self.open_edit_overlay(d)
        ).pack(pady=5)
        ctk.CTkButton(
            actions, text="🗑️ Supprimer", width=120, height=35,
            fg_color=PALE_RED, hover_color=PALE_RED_HOVER, font=("Arial", 11, "bold"),
            command=lambda d=pu: self.delete_publisher(d["id"])
        ).pack(pady=5)

    # ---------- CRUD ----------
    def open_create_overlay(self):
        PublisherOverlayWindow(self, on_validate=self.save_publisher).show()

    def open_edit_overlay(self, pu_dict: dict):
        PublisherOverlayWindow(self, on_validate=self.save_publisher, publisher_data=pu_dict).show()

    def save_publisher(self, data, is_edit=False):
        """
        Insert / Update Publisher en base.
        Champs : _name (String). Relation: books (pour le comptage).
        """
        session = get_session()
        try:
            # Anti-doublon simple (optionnel)
            existing = session.query(Publisher).filter(
                Publisher._name == data["name"]
            ).first()
            if existing and (not is_edit or existing._id != data["id"]):
                self._toast_error("Un éditeur portant ce nom existe déjà.")
                return

            if is_edit and data["id"] is not None:
                pu = session.query(Publisher).filter_by(_id=data["id"]).first()
                if not pu:
                    self._toast_error(f"Éditeur ID {data['id']} introuvable.")
                    return
                pu._name = data["name"]
                session.commit()
                print(f"✅ Éditeur modifié : {pu._name} (ID: {pu._id})")
            else:
                new_pu = Publisher(_name=data["name"])
                session.add(new_pu)
                session.commit()
                print(f"✅ Nouvel éditeur créé : {new_pu._name} (ID: {new_pu._id})")

            self.refresh_publishers_list()

        except Exception as e:
            session.rollback()
            print(f"❌ Erreur save_publisher : {e}")
            import traceback; traceback.print_exc()
            self._toast_error("Erreur lors de l’enregistrement.")
        finally:
            session.close()

    def delete_publisher(self, pu_id: int):
        session = get_session()
        try:
            pu = session.query(Publisher).filter_by(_id=pu_id).first()
            if not pu:
                self._toast_error("Éditeur introuvable.")
                return

            # Empêcher la suppression si des livres y sont liés
            nb = len(getattr(pu, "books", []) or [])
            if nb > 0:
                self._toast_error(f"Impossible de supprimer : {nb} livre(s) associé(s).")
                return

            name = getattr(pu, "_name", "") or f"Éditeur #{pu_id}"
            session.delete(pu)
            session.commit()
            print(f"✅ Éditeur supprimé : {name} (ID: {pu_id})")
            self.refresh_publishers_list()

        except Exception as e:
            session.rollback()
            print(f"❌ Erreur delete_publisher : {e}")
            import traceback; traceback.print_exc()
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


app = EditeursApp()
app.mainloop()
