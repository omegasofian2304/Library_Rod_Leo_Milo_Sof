import customtkinter as ctk
from PIL import Image
from PIL.ImageOps import expand

# Couleurs
dark_grey = "#BFBFBF"
light_grey = "#D9D9D9"
blue_violet = "#6F64FF"
green = "#B5E6AB"
red = "#FFBFBF"

# Création de l'application
app = ctk.CTk()
app.geometry("1440x900")
app.title("Créer/Modifier un membre")

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
lb_account = ctk.CTkLabel(master=fr_account, text="Compte")
lb_account.pack()

# Menu
fr_menu = ctk.CTkFrame(master=fr_header_right, fg_color="#DFDFDF", height=80)
fr_menu.pack(fill="both", expand=True, padx=10)
lbl_menu = ctk.CTkLabel(
    master=fr_menu,
    text="________\n\n________\n\n________",
    font=("Arial", 16, "bold")
)
lbl_menu.pack(ipadx=40)

# ======================
# CONTENT
# ======================
fr_content = ctk.CTkFrame(master=app, fg_color=dark_grey, corner_radius=20)
fr_content.pack(fill="both", expand=True, padx=40, pady=(0, 40))

# Frame principal du formulaire
fr_form = ctk.CTkFrame(master=fr_content, fg_color=light_grey, corner_radius=20)
fr_form.pack(fill="both", expand=True, padx=80, pady=80)

# Champs du formulaire
fr_fields = ctk.CTkFrame(master=fr_form, fg_color=light_grey)
fr_fields.pack(expand=True, pady=40,fill="both",padx=40)

# ID
lbl_id = ctk.CTkLabel(master=fr_fields, text="ID :", font=("Arial", 14))
lbl_id.grid(row=0, column=0, sticky="w", padx=20, pady=15)
entry_id = ctk.CTkEntry(master=fr_fields, width=400, height=40)
entry_id.grid(row=0, column=1, padx=20, pady=15)

# NOM
lbl_nom = ctk.CTkLabel(master=fr_fields, text="NOM:", font=("Arial", 14))
lbl_nom.grid(row=1, column=0, sticky="w", padx=20, pady=15)
entry_nom = ctk.CTkEntry(master=fr_fields, width=400, height=40)
entry_nom.grid(row=1, column=1, padx=20, pady=15)

# PRÉNOM
lbl_prenom = ctk.CTkLabel(master=fr_fields, text="PRÉNOM:", font=("Arial", 14))
lbl_prenom.grid(row=2, column=0, sticky="w", padx=20, pady=15)
entry_prenom = ctk.CTkEntry(master=fr_fields, width=400, height=40)
entry_prenom.grid(row=2, column=1, padx=20, pady=15)

# E-MAIL
lbl_email = ctk.CTkLabel(master=fr_fields, text="E-MAIL:", font=("Arial", 14))
lbl_email.grid(row=3, column=0, sticky="w", padx=20, pady=15)
entry_email = ctk.CTkEntry(master=fr_fields, width=400, height=40)
entry_email.grid(row=3, column=1, padx=20, pady=15)

# ======================
# Boutons bas
# ======================
fr_buttons = ctk.CTkFrame(master=fr_form, fg_color=light_grey)
fr_buttons.pack(side="bottom", pady=20,expand=True,fill="both")

btn_annuler = ctk.CTkButton(
    master=fr_buttons,
    text="ANNULER",
    fg_color=red,
    hover_color="#FF9999",
    width=200,
    height=50,
    font=("Arial", 14, "bold")
)
btn_annuler.pack(side="left", padx=20)

btn_valider = ctk.CTkButton(
    master=fr_buttons,
    text="VALIDER",
    fg_color=green,
    hover_color="#9FD695",
    width=200,
    height=50,
    font=("Arial", 14, "bold")
)
btn_valider.pack(side="right", padx=20)

# Lancement de l'application
app.mainloop()