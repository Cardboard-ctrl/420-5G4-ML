import customtkinter as ctk

import theme
from ui.pages.base import BasePage
from ui.widgets import BookCard, EmptyState, IconTextButton, SearchBar


class BooksPage(BasePage):
    page_key = "books"
    page_title = "Livres"

    def __init__(self, master, app):
        super().__init__(master, app)
        self._available_only = False
        self._search_by_author = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        toolbar.grid_columnconfigure(0, weight=1, minsize=220)

        self.search_bar = SearchBar(
            toolbar,
            placeholder="Recherche : Par Titre",
            command=self.refresh,
        )
        self.search_bar.grid(row=0, column=0, sticky="ew")

        self.author_button = IconTextButton(
            toolbar,
            "swap",
            "Par Auteur",
            command=self.toggle_search_mode,
        )
        self.author_button.grid(row=0, column=1, padx=(12, 0))

        self.all_button = self._action_button(
            toolbar, "Tous les livres", lambda: self.set_filter(False)
        )
        self.all_button.grid(row=0, column=2, padx=(12, 0))
        self.available_button = self._action_button(
            toolbar, "Livres Disponibles", lambda: self.set_filter(True)
        )
        self.available_button.grid(row=0, column=3, padx=(12, 0))

        self.add_button = IconTextButton(
            toolbar,
            "add_book",
            "Ajouter un livre",
            disabled=True,
            width=160,
        )
        self.add_button.grid(row=0, column=4, padx=(12, 0))

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=theme.COLORS["button"],
            scrollbar_button_hover_color=theme.COLORS["button_hover"],
        )
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

        self._update_filter_buttons()

    def _action_button(self, master, text, command):
        return ctk.CTkButton(
            master,
            text=text,
            command=command,
            width=160,
            height=32,
            font=theme.small_font(),
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["button"],
            hover_color=theme.COLORS["button_hover"],
            text_color=theme.COLORS["text"],
        )

    def _update_filter_buttons(self):
        active_text = ("#FFFFFF", "#101828")
        inactive_text = theme.COLORS["text"]
        all_active = not self._available_only
        available_active = self._available_only
        self.all_button.configure(
            fg_color=theme.COLORS["accent"] if all_active else theme.COLORS["button"],
            text_color=active_text if all_active else inactive_text,
        )
        self.available_button.configure(
            fg_color=theme.COLORS["accent"]
            if available_active
            else theme.COLORS["button"],
            text_color=active_text if available_active else inactive_text,
        )

    def set_filter(self, available_only):
        self._available_only = available_only
        self._update_filter_buttons()
        self.refresh()

    def toggle_search_mode(self):
        self._search_by_author = not self._search_by_author
        if self._search_by_author:
            self.search_bar.set_placeholder("Recherche : Par Auteur")
            self.author_button.configure(text="Par Titre")
        else:
            self.search_bar.set_placeholder("Recherche : Par Titre")
            self.author_button.configure(text="Par Auteur")
        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        if self.library is None:
            EmptyState(
                self.scroll,
                "Bibliothèque indisponible. Vérifiez le module C++ et le répertoire data.",
            ).pack(fill="x")
            return

        term = self.search_bar.get()
        try:
            if term:
                if self._search_by_author:
                    books = self.library.search_by_author(term)
                else:
                    books = self.library.search_by_title(term)
            else:
                books = self.library.list_books(available_only=self._available_only)
        except Exception as exc:
            EmptyState(self.scroll, f"Erreur de chargement : {exc}").pack(fill="x")
            return

        if term and self._available_only:
            books = [book for book in books if book["available"]]

        if not books:
            EmptyState(self.scroll, "Aucun livre à afficher.").pack(fill="x")
            return

        for book in books:
            BookCard(self.scroll, book).pack(fill="x", pady=6)
