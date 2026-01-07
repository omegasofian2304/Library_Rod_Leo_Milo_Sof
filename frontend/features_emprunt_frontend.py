import customtkinter as ctk
from overlay_book_select import OverlayWindow
from PIL import Image
# Couleurs
dark_grey = "#BFBFBF"
light_grey = "#D9D9D9"
blue_violet = "#6F64FF"
green = "#B5E6AB"
red = "#FFBFBF"

# Création de l'application
app = ctk.CTk()
app.geometry("1440x900")
app.title("Emprunt")


# ======================
# Classe Book (livre)
# ======================
class Book(ctk.CTkFrame):
    def __init__(self, master, index, book_id, book_name, **kwargs):
        super().__init__(master, **kwargs)

        # Label du livre
        lbl = ctk.CTkLabel(self, text=f"{book_id} - {book_name}")
        lbl.pack(side="left", padx=10, pady=10)

        # Bouton supprimer
        self.delete_btn = ctk.CTkButton(
            self,
            text="Supprimer",
            command=self.destroy  # <-- correcte
        )
        self.delete_btn.pack(side="right", padx=10, pady=10)


# ======================
# HEADER
# ======================
fr_header = ctk.CTkFrame(master=app, fg_color=dark_grey, corner_radius=20, height=150)
fr_header.pack(padx=40, pady=40, anchor="w")


# Logo
fr_logo = ctk.CTkFrame(master=fr_header, fg_color="transparent", height=125, width=125)
fr_logo.pack(side="left", padx=20, pady=20)

# Image du logo
logo_image = ctk.CTkImage(
    light_image=Image.open("logo.png"),
    dark_image=Image.open("logo.png"),
    size=(125, 125)
)
lbl_logo = ctk.CTkLabel(master=fr_logo, image=logo_image, text="")
lbl_logo.pack(expand=True)

# Contenu droit du header
fr_header_right = ctk.CTkFrame(master=fr_header, fg_color="transparent")
fr_header_right.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Frame compte (account)
fr_account = ctk.CTkFrame(master=fr_header_right, fg_color="#CFCFCF", height=30)
fr_account.pack(fill="x", pady=(0, 10))
lb_account = ctk.CTkLabel(master=fr_account, text="account")
lb_account.pack()

# Menu
fr_menu = ctk.CTkFrame(master=fr_header_right, fg_color="#DFDFDF", height=80)
fr_menu.pack(fill="both", expand=True, padx=10)
lbl_menu = ctk.CTkLabel(master=fr_menu, text="________\n\n________\n\n________\n", font=("Arial", 16, "bold"))
lbl_menu.pack(ipadx=40)


# ======================
# CONTENT
# ======================
fr_content = ctk.CTkFrame(master=app, fg_color=dark_grey, corner_radius=20)
fr_content.pack(fill="both", expand=True, padx=10, pady=10)

fr_main_content = ctk.CTkFrame(master=fr_content, fg_color=dark_grey)
fr_main_content.pack(fill="both", expand=True, padx=20)

# ===== Livres =====
fr_book = ctk.CTkFrame(master=fr_main_content, fg_color=dark_grey)
fr_book.pack(fill="x", padx=(40, 20), pady=40, side="left", anchor="nw")

fr_book_content = ctk.CTkScrollableFrame(master=fr_book, fg_color=light_grey, height=215, width=575)
fr_book_content.pack(padx=20, pady=10, side="top", anchor="w")


# ===== Clients =====
fr_customer = ctk.CTkFrame(master=fr_main_content, fg_color=dark_grey)
fr_customer.pack(fill="x", padx=(40, 20), pady=40, side="right", anchor="ne")

fr_customer_content = ctk.CTkFrame(master=fr_customer, fg_color=light_grey, height=360, width=575)
fr_customer_content.pack(padx=20, pady=10, anchor="n")

btn_modif_customer = ctk.CTkButton(master=fr_customer, fg_color=blue_violet, height=60, width=260, text="Modifier")
btn_modif_customer.pack(padx=20, pady=10, side="top", anchor="w")


# ===== Boutons bas =====
fr_btn = ctk.CTkFrame(master=fr_content, fg_color=dark_grey)
fr_btn.pack(side="bottom", fill="x", pady=(10, 10))

btn_return = ctk.CTkButton(master=fr_btn, fg_color=red, height=60, width=260, text="Retour")
btn_return.pack(side="left", padx=20, pady=10)

btn_valide_borrow = ctk.CTkButton(master=fr_btn, fg_color=green, height=60, width=260, text="Valider")
btn_valide_borrow.pack(side="right", padx=20, pady=10)


# ======================
# Logique Ajout Livre
# ======================
book_list = []
livre_count = 0
def open_overlay():
    overlay = OverlayWindow(app)  # ← crée une instance avec l’app comme parent
    overlay.show()               # ← affiche le Toplevel


def AjoutLivre(book_id, book_name):
    global livre_count
    livre_count += 1

    new_book = Book(
        fr_book_content,
        index=livre_count,
        book_id=book_id,
        book_name=book_name,
        fg_color=dark_grey,
        corner_radius=10
    )
    new_book.pack(padx=20, pady=10, anchor="w")
    book_list.append(new_book)


btn_add_book = ctk.CTkButton(
    master=fr_book,
    fg_color=blue_violet,
    height=60,
    width=260,
    text="Ajouter",
    command=lambda: OverlayWindow(app, on_select=AjoutLivre).show()
)
btn_add_book.pack(padx=20, pady=10, side="top", anchor="w")






# ======================
# Lancement de l’application
# ======================
app.mainloop()
