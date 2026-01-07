import customtkinter as ctk
from PIL import Image

# Couleurs
dark_grey = "#BFBFBF"
light_grey = "#D9D9D9"
blue_violet = "#6F64FF"
green = "#B5E6AB"
red = "#FFBFBF"

# Données de test
members_data = [
    [1, "Dupont", "Jean", "jean.dupont@email.com"],
    [2, "Martin", "Sophie", "sophie.martin@email.com"],
    [3, "Bernard", "Luc", "luc.bernard@email.com"]
]

# Création de l'application
app = ctk.CTk()
app.geometry("1440x900")
app.title("Membres")

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

# Frame pour le bouton "Créer nouveau membre"
fr_top_actions = ctk.CTkFrame(master=fr_content, fg_color=dark_grey)
fr_top_actions.pack(fill="x", padx=40, pady=(30, 10))

btn_create_member = ctk.CTkButton(
    master=fr_top_actions,
    text="CRÉÉ NOUVEAU MEMBRE  +",
    fg_color=blue_violet,
    hover_color="#5F54EF",
    width=300,
    height=50,
    font=("Arial", 14, "bold")
)
btn_create_member.pack(side="right")

# Frame pour la recherche
fr_search = ctk.CTkFrame(master=fr_content, fg_color=dark_grey)
fr_search.pack(fill="x", padx=40, pady=10)

entry_search = ctk.CTkEntry(
    master=fr_search,
    placeholder_text="🔍  ID, NOM, PRÉNOM, E-MAIL",
    height=45,
    font=("Arial", 12)
)
entry_search.pack(fill="x")


# ======================
# Classe Member (membre dans la liste)
# ======================
class MemberRow(ctk.CTkFrame):
    def __init__(self, master, member_id, nom, prenom, email, **kwargs):
        super().__init__(master, **kwargs)

        # Frame principal de la ligne
        self.configure(fg_color=light_grey, corner_radius=10)

        # Label avec les infos du membre
        lbl_info = ctk.CTkLabel(
            self,
            text=f"ID, NOM, PRÉNOM, E-MAIL",
            font=("Arial", 12),
            text_color="#808080"
        )
        lbl_info.pack(side="left", padx=20, pady=15)

        # Frame pour les boutons
        fr_buttons = ctk.CTkFrame(master=self, fg_color="transparent")
        fr_buttons.pack(side="right", padx=20)

        # Bouton Modifier
        btn_modifier = ctk.CTkButton(
            master=fr_buttons,
            text="Modifier",
            fg_color=blue_violet,
            hover_color="#5F54EF",
            width=120,
            height=40,
            font=("Arial", 12, "bold")
        )
        btn_modifier.pack(side="left", padx=5)

        # Bouton Emprunt
        btn_emprunt = ctk.CTkButton(
            master=fr_buttons,
            text="Emprunt  +",
            fg_color=blue_violet,
            hover_color="#5F54EF",
            width=120,
            height=40,
            font=("Arial", 12, "bold")
        )
        btn_emprunt.pack(side="left", padx=5)


# Frame scrollable pour la liste des membres
fr_members_list = ctk.CTkScrollableFrame(
    master=fr_content,
    fg_color=dark_grey,
    corner_radius=10
)
fr_members_list.pack(fill="both", expand=True, padx=40, pady=(20, 40))

# Ajouter les membres de test
for member in members_data:
    member_row = MemberRow(
        master=fr_members_list,
        member_id=member[0],
        nom=member[1],
        prenom=member[2],
        email=member[3]
    )
    member_row.pack(fill="x", padx=10, pady=8)

# Lancement de l'application
app.mainloop()