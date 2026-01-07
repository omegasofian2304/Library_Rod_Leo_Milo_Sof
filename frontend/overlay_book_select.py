import customtkinter as ctk
dark_grey = "#BFBFBF"
light_grey = "#D9D9D9"
blue_violet = "#6F64FF"
green = "#B5E6AB"
red = "#FFBFBF"

Books_data = [[1,"le bonjour"],
             [2,"c'est pas bien"],
             [3,"non non non"]]


def Valider():
    return()
    win.destroy()
class Books_info(ctk.CTkFrame):
    def __init__(self, master, texte_id, texte_name, callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.texte_id = texte_id
        self.texte_name = texte_name
        self.callback = callback  # Fonction à appeler au clic

        # Labels
        lbl_id = ctk.CTkLabel(self, text=str(texte_id))
        lbl_id.grid(row=0, column=0, padx=20)

        lbl_name = ctk.CTkLabel(self, text=texte_name)
        lbl_name.grid(row=0, column=1, padx=20)

        # Bouton "Choisir"
        btn_choose = ctk.CTkButton(self, text="Choisir", command=self.on_choose)
        btn_choose.grid(row=0, column=2, padx=20)

    def on_choose(self):
        if self.callback:
            # Appelle la fonction callback en lui passant les infos du livre
            self.callback(self.texte_id, self.texte_name)



class OverlayWindow:
    def __init__(self, parent, on_select=None):
        self.parent = parent
        self.on_select = on_select  # Callback à exécuter quand un livre est choisi

    def show(self):
        self.win = ctk.CTkToplevel(self.parent)
        self.win.title("Overlay")
        self.win.geometry("1440x900")

        btn_close = ctk.CTkButton(self.win, text="Fermer", command=self.win.destroy)
        btn_close.pack(pady=10)

        fr_content = ctk.CTkFrame(master=self.win, fg_color=dark_grey, corner_radius=20)
        fr_content.pack(fill="both", expand=True, padx=10, pady=10)

        fr_book_content = ctk.CTkScrollableFrame(master=fr_content, fg_color=light_grey, height=215)
        fr_book_content.pack(fill="both", expand=True, padx=20, pady=10)

        # Ajouter chaque livre avec le bouton "Choisir"
        for book in Books_data:
            newBook = Books_info(
                master=fr_book_content,
                texte_id=book[0],
                texte_name=book[1],
                fg_color=dark_grey,
                callback=self.book_selected  # <-- on passe la fonction à chaque frame
            )
            newBook.pack(fill="x", padx=20, pady=10)

        # Mettre au premier plan
        self.win.lift()
        self.win.attributes('-topmost', True)
        self.win.focus_force()
        self.win.after(100, lambda: self.win.attributes('-topmost', False))

    def book_selected(self, texte_id, texte_name):
        # Ici on appelle le callback fourni par la fenêtre principale
        if self.on_select:
            self.on_select(texte_id, texte_name)

        # Puis on ferme l'overlay
        self.win.destroy()

