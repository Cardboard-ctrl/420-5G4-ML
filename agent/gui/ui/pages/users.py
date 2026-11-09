import customtkinter as ctk

import theme
from ui.pages.base import BasePage
from ui.widgets import EmptyState, IconButton, UserCard


class UsersPage(BasePage):
    page_key = "users"
    page_title = "Utilisateurs"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        toolbar.grid_columnconfigure(0, weight=1)

        self.add_button = IconButton(toolbar, "user_plus", size=26, disabled=True)
        self.add_button.grid(row=0, column=1, sticky="e")

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=theme.COLORS["button"],
            scrollbar_button_hover_color=theme.COLORS["button_hover"],
        )
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

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
