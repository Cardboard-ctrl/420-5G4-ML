import customtkinter as ctk

import theme
from ui.pages.base import BasePage
from ui.widgets import EmptyState, IconButton, UserCard


class AddUserDialog(ctk.CTkToplevel):
    def __init__(self, master, on_submit):
        super().__init__(master, fg_color=theme.COLORS["window"])
        self.title("Ajouter un utilisateur")
        self.geometry("430x330")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.on_submit = on_submit

        content = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS["surface"],
            corner_radius=theme.RADIUS["card"],
        )
        content.pack(fill="both", expand=True, padx=24, pady=24)
        content.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            content,
            text="Ajouter un utilisateur",
            font=theme.font(18, "bold"),
            text_color=theme.COLORS["text"],
        ).grid(row=0, column=0, columnspan=2, pady=(20, 14), padx=20)

        self.name_entry = self._field(content, 1, "Nom")
        self.id_entry = self._field(content, 2, "ID utilisateur")

        self.error = ctk.CTkLabel(
            content,
            text="",
            font=theme.small_font(),
            text_color=theme.COLORS["danger"],
            wraplength=340,
            justify="left",
        )
        self.error.grid(row=3, column=0, columnspan=2, sticky="w", padx=24, pady=(8, 0))

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.grid(row=4, column=0, columnspan=2, pady=(18, 20))

        ctk.CTkButton(
            buttons,
            text="Annuler",
            command=self.destroy,
            width=120,
            height=32,
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["button"],
            hover_color=theme.COLORS["button_hover"],
            text_color=theme.COLORS["text"],
            font=theme.small_font(),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            buttons,
            text="Ajouter",
            command=self.submit,
            width=120,
            height=32,
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["accent"],
            hover_color=theme.COLORS["button_hover"],
            text_color=("#FFFFFF", "#101828"),
            font=theme.small_font(),
        ).pack(side="left")

        self.bind("<Return>", lambda _event: self.submit())
        self.name_entry.focus_set()

    def _field(self, master, row, label):
        ctk.CTkLabel(
            master,
            text=label,
            font=theme.body_font(),
            text_color=theme.COLORS["text"],
            anchor="w",
        ).grid(row=row, column=0, sticky="w", padx=(24, 12), pady=6)
        entry = ctk.CTkEntry(
            master,
            height=34,
            corner_radius=theme.RADIUS["button"],
            border_width=0,
            fg_color=theme.COLORS["surface_alt"],
            text_color=theme.COLORS["text"],
            font=theme.body_font(),
        )
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=6)
        return entry

    def submit(self):
        name = self.name_entry.get().strip()
        user_id = self.id_entry.get().strip()
        if not name or not user_id:
            self.error.configure(text="Le nom et l'ID sont obligatoires.")
            return

        error = self.on_submit(name, user_id)
        if error:
            self.error.configure(text=error)
            return

        self.destroy()


class UsersPage(BasePage):
    page_key = "users"
    page_title = "Utilisateurs"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        toolbar.grid_columnconfigure(0, weight=1)

        self.add_button = IconButton(
            toolbar,
            "user_plus",
            size=26,
            command=self.open_add_dialog,
        )
        self.add_button.grid(row=0, column=1, sticky="e")

        self.feedback = ctk.CTkLabel(
            self,
            text="",
            font=theme.body_font(),
            text_color=theme.COLORS["muted"],
        )
        self.feedback.grid(row=1, column=0, sticky="w", pady=(0, 8))

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=theme.COLORS["button"],
            scrollbar_button_hover_color=theme.COLORS["button_hover"],
        )
        self.scroll.grid(row=2, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

    def _set_feedback(self, text, error=False):
        self.feedback.configure(
            text=text,
            text_color=theme.COLORS["danger"] if error else theme.COLORS["muted"],
        )

    def open_add_dialog(self):
        if self.library is None:
            self._set_feedback("Bibliothèque indisponible.", error=True)
            return
        AddUserDialog(self.app, self.add_user)

    def add_user(self, name, user_id):
        try:
            added = self.library.add_user(name, user_id)
        except Exception as exc:
            return f"Erreur : {exc}"

        if not added:
            return "Cet ID utilisateur existe déjà."

        self._set_feedback("Utilisateur ajouté. Pensez à sauvegarder.")
        self.refresh()
        return None

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        if self.library is None:
            EmptyState(
                self.scroll,
                "Bibliothèque indisponible. Vérifiez le module C++ et le répertoire data.",
            ).pack(fill="x")
            return

        try:
            users = self.library.list_users()
        except Exception as exc:
            EmptyState(self.scroll, f"Erreur de chargement : {exc}").pack(fill="x")
            return

        if not users:
            EmptyState(self.scroll, "Aucun utilisateur à afficher.").pack(fill="x")
            return

        for user in users:
            UserCard(self.scroll, user).pack(fill="x", pady=6)
