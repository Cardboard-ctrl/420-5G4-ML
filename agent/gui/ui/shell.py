import sys

import customtkinter as ctk

import theme
from ui.nav_bar import NavBar
from ui.pages.books import BooksPage, MessageDialog
from ui.pages.settings import SettingsPage
from ui.pages.users import UsersPage


class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Bibliothèque",
            font=theme.title_font(),
            text_color=theme.COLORS["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        self.subtitle = ctk.CTkLabel(
            self,
            text="",
            font=theme.subtitle_font(),
            text_color=theme.COLORS["muted"],
            anchor="w",
        )
        self.subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

    def set_subtitle(self, text):
        self.subtitle.configure(text=text)


class BibliothequeApp(ctk.CTk):
    def __init__(self, data_dir):
        super().__init__(fg_color=theme.COLORS["window"])
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("Light")

        self.title("Bibliothèque")
        self.geometry("1320x900")
        self.minsize(1000, 700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.library, self.library_error = self._create_library(data_dir)
        if self.library_error:
            print(
                f"Bibliothèque indisponible : {self.library_error}",
                file=sys.stderr,
            )

        self.header = Header(self)
        self.header.grid(row=0, column=0, sticky="ew", padx=32, pady=(26, 16))

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=32)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {
            "books": BooksPage(self.content, self),
            "users": UsersPage(self.content, self),
            "settings": SettingsPage(self.content, self),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()

        self.nav = NavBar(self, on_change=self.show_page)
        self.nav.grid(row=2, column=0, sticky="ew")

        self.current_page = None
        self.show_page("books")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _create_library(self, data_dir):
        try:
            from bibliotheque_api import Bibliotheque

            return Bibliotheque(data_dir), None
        except Exception as exc:
            return None, str(exc)

    def show_page(self, key):
        page = self.pages.get(key)
        if page is None:
            return

        if self.current_page is not None:
            self.pages[self.current_page].grid_remove()

        page.grid()
        page.on_show()
        self.header.set_subtitle(page.page_title)
        self.nav.set_active(key)
        self.current_page = key

    def on_close(self):
        if self.library is not None:
            try:
                saved = self.library.save()
            except Exception as exc:
                MessageDialog(
                    self,
                    "Sauvegarde impossible",
                    f"Les données n'ont pas pu être sauvegardées : {exc}",
                )
                return
            if not saved:
                MessageDialog(
                    self,
                    "Sauvegarde impossible",
                    "Les données n'ont pas pu être sauvegardées. Fermeture annulée.",
                )
                return
        self.destroy()
