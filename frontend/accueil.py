"""
Auteur : Léo del Duca
Date : 03.12.2025
Projet : Un gestionnaire  de livre pour une librairie
"""

import customtkinter as ctk

# Configuration de base de la fenêtre
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1100x650")
app.title("Magic Books")

# Frame de fond
bg = ctk.CTkFrame(app, fg_color="#d9ad7c", corner_radius=0)
bg.pack(fill="both", expand=True)

# En-tête avec zone compte (placeholder, sans fonctionnalité)
header = ctk.CTkFrame(bg, fg_color="#e5e5e5", height=80)
header.pack(fill="x", padx=20, pady=20)
header.pack_propagate(False)

logo_label = ctk.CTkLabel(header, text="MAGIC\nBOOKS", font=("Arial", 20, "bold"))
logo_label.pack(side="left", padx=20)

account_frame = ctk.CTkFrame(header, fg_color="#cccccc", width=180, height=60, corner_radius=10)
account_frame.pack(side="right", padx=20)
account_frame.pack_propagate(False)

# Burger menu button
burger_button = ctk.CTkButton(account_frame, text="≡", width=40, height=40)
burger_button.pack(side="right", padx=10, pady=10)

account_label = ctk.CTkLabel(account_frame, text="Compte", font=("Arial", 16, "bold"))
account_label.pack(pady=5)

# Side menu (hidden by default)
menu_frame = ctk.CTkFrame(app, width=250, fg_color="#f2f2f2", corner_radius=0)
menu_visible = False


# Menu toggle function
def toggle_menu():
    global menu_visible
    if menu_visible:
        menu_frame.place_forget()
        menu_visible = False
    else:
        menu_frame.place(x=0, y=0, relheight=1)
        menu_visible = True


burger_button.configure(command=toggle_menu)

# Menu title
menu_title = ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 22, "bold"))
menu_title.pack(pady=20)


# Menu buttons (no functionality)
menu_items = ["Livres", "Membres", "Emprunt", "Employés", "Auteur", "Edition"]


for item in menu_items:
    btn = ctk.CTkButton(menu_frame, text=item, width=180)
    btn.pack(pady=8)

# Section du titre de la recommandation
reco_frame = ctk.CTkFrame(bg, fg_color="#6C5CE7", corner_radius=10)
reco_frame.pack(pady=10)

reco_label = ctk.CTkLabel(reco_frame, text="Recommandation de la semaine :", font=("Arial", 18, "bold"), text_color="white")
reco_label.pack(padx=20, pady=10)

# Contenu principal
content = ctk.CTkFrame(bg, fg_color="#e6c39f", corner_radius=15)
content.pack(fill="both", expand=True, padx=30, pady=10)

# Placeholder pour l'image à gauche
image_frame = ctk.CTkFrame(content, width=300, height=420, fg_color="#ffffff", corner_radius=10)
image_frame.pack(side="left", padx=30, pady=30)
image_frame.pack_propagate(False)

image_label = ctk.CTkLabel(image_frame, text="Image du livre\n(placeholder)", font=("Arial", 16))
image_label.pack(expand=True)

# Informations texte
info_frame = ctk.CTkFrame(content, fg_color="#e6c39f")
info_frame.pack(side="left", padx=20, pady=30)

# titre du livre
label_titre = ctk.CTkLabel(info_frame, text="Titre :", font=("Arial", 26, "bold"))
label_titre.grid(row=0, column=0, sticky="w", pady=10)
value_titre = ctk.CTkLabel(info_frame, text="Cyrano de Bergerac", font=("Arial", 26))
value_titre.grid(row=0, column=1, sticky="w", padx=20)

# Éditeur
label_editeur = ctk.CTkLabel(info_frame, text="Éditeur :", font=("Arial", 26, "bold"))
label_editeur.grid(row=1, column=0, sticky="w", pady=10)
value_editeur = ctk.CTkLabel(info_frame, text="Voir de près", font=("Arial", 26))
value_editeur.grid(row=1, column=1, sticky="w", padx=20)

# Auteur
label_auteur = ctk.CTkLabel(info_frame, text="Auteur :", font=("Arial", 26, "bold"))
label_auteur.grid(row=2, column=0, sticky="w", pady=10)
value_auteur = ctk.CTkLabel(info_frame, text="Edmond Rostand", font=("Arial", 26))
value_auteur.grid(row=2, column=1, sticky="w", padx=20)

app.mainloop()
