import customtkinter as ctk

import theme
from ui.pages.base import BasePage
from ui.widgets import BookCard, EmptyState, IconTextButton, SearchBar


class MessageDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message):
        super().__init__(master, fg_color=theme.COLORS["window"])
        self.title(title)
        self.geometry("440x230")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        content = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS["surface"],
            corner_radius=theme.RADIUS["card"],
        )
        content.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            content,
            text=title,
            font=theme.font(18, "bold"),
            text_color=theme.COLORS["text"],
        ).pack(pady=(20, 10), padx=20)

        ctk.CTkLabel(
            content,
            text=message,
            font=theme.body_font(),
            text_color=theme.COLORS["text"],
            wraplength=350,
            justify="left",
        ).pack(pady=(0, 16), padx=20)

        ctk.CTkButton(
            content,
            text="Fermer",
            command=self.destroy,
            width=120,
            height=32,
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["button"],
            hover_color=theme.COLORS["button_hover"],
            text_color=theme.COLORS["text"],
            font=theme.small_font(),
        ).pack(pady=(0, 20))

        self.bind("<Escape>", lambda _event: self.destroy())


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message, on_confirm):
        super().__init__(master, fg_color=theme.COLORS["window"])
        self.title(title)
        self.geometry("440x250")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.on_confirm = on_confirm

        content = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS["surface"],
            corner_radius=theme.RADIUS["card"],
        )
        content.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            content,
            text=title,
            font=theme.font(18, "bold"),
            text_color=theme.COLORS["text"],
        ).pack(pady=(20, 10), padx=20)

        ctk.CTkLabel(
            content,
            text=message,
            font=theme.body_font(),
            text_color=theme.COLORS["text"],
            wraplength=350,
            justify="left",
        ).pack(pady=(0, 16), padx=20)

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.pack(pady=(0, 20))

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
            text="Supprimer",
            command=self.confirm,
            width=120,
            height=32,
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["danger"],
            hover_color=theme.COLORS["button_hover"],
            text_color="#FFFFFF",
            font=theme.small_font(),
        ).pack(side="left")

        self.bind("<Escape>", lambda _event: self.destroy())

    def confirm(self):
        self.destroy()
        self.on_confirm()


class AddBookDialog(ctk.CTkToplevel):
    def __init__(self, master, on_submit):
        super().__init__(master, fg_color=theme.COLORS["window"])
        self.title("Ajouter un livre")
        self.geometry("450x400")
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
            text="Ajouter un livre",
            font=theme.font(18, "bold"),
            text_color=theme.COLORS["text"],
        ).grid(row=0, column=0, columnspan=2, pady=(20, 14), padx=20)

        self.title_entry = self._field(content, 1, "Titre")
        self.author_entry = self._field(content, 2, "Auteur")
        self.isbn_entry = self._field(content, 3, "ISBN")

        self.error = ctk.CTkLabel(
            content,
            text="",
            font=theme.small_font(),
            text_color=theme.COLORS["danger"],
            wraplength=360,
            justify="left",
        )
        self.error.grid(row=4, column=0, columnspan=2, sticky="w", padx=24, pady=(8, 0))

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.grid(row=5, column=0, columnspan=2, pady=(18, 20))

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
        self.title_entry.focus_set()

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
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        if not title or not author or not isbn:
            self.error.configure(
                text="Le titre, l'auteur et l'ISBN sont obligatoires."
            )
            return

        error = self.on_submit(title, author, isbn)
        if error:
            self.error.configure(text=error)
            return

        self.destroy()


class BorrowDialog(ctk.CTkToplevel):
    def __init__(self, master, book, users, on_submit):
        super().__init__(master, fg_color=theme.COLORS["window"])
        self.title("Emprunter un livre")
        self.geometry("450x330")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.on_submit = on_submit
        self.display_to_id = {
            f"{user['name']} ({user['user_id']})": user["user_id"] for user in users
        }

        content = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS["surface"],
            corner_radius=theme.RADIUS["card"],
        )
        content.pack(fill="both", expand=True, padx=24, pady=24)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            content,
            text="Emprunter un livre",
            font=theme.font(18, "bold"),
            text_color=theme.COLORS["text"],
        ).grid(row=0, column=0, pady=(20, 6), padx=20)

        ctk.CTkLabel(
            content,
            text=f"« {book['title']} » — ISBN {book['isbn']}",
            font=theme.body_font(),
            text_color=theme.COLORS["muted"],
            wraplength=360,
            justify="center",
        ).grid(row=1, column=0, pady=(0, 16), padx=20)

        ctk.CTkLabel(
            content,
            text="Utilisateur",
            font=theme.body_font(),
            text_color=theme.COLORS["text"],
            anchor="w",
        ).grid(row=2, column=0, sticky="w", padx=24, pady=(0, 6))

        self.user_menu = ctk.CTkOptionMenu(
            content,
            values=list(self.display_to_id),
            height=34,
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["surface_alt"],
            button_color=theme.COLORS["button"],
            button_hover_color=theme.COLORS["button_hover"],
            text_color=theme.COLORS["text"],
            font=theme.body_font(),
            dropdown_font=theme.body_font(),
            dropdown_fg_color=theme.COLORS["surface_alt"],
            dropdown_hover_color=theme.COLORS["button"],
            dropdown_text_color=theme.COLORS["text"],
        )
        self.user_menu.grid(row=3, column=0, sticky="ew", padx=24)

        self.error = ctk.CTkLabel(
            content,
            text="",
            font=theme.small_font(),
            text_color=theme.COLORS["danger"],
            wraplength=360,
            justify="left",
        )
        self.error.grid(row=4, column=0, sticky="w", padx=24, pady=(8, 0))

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.grid(row=5, column=0, pady=(18, 20))

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
            text="Emprunter",
            command=self.submit,
            width=120,
            height=32,
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["accent"],
            hover_color=theme.COLORS["button_hover"],
            text_color=("#FFFFFF", "#101828"),
            font=theme.small_font(),
        ).pack(side="left")

        self.bind("<Escape>", lambda _event: self.destroy())

    def submit(self):
        user_id = self.display_to_id.get(self.user_menu.get())
        if not user_id:
            self.error.configure(text="Sélectionnez un utilisateur.")
            return

        error = self.on_submit(user_id)
        if error:
            self.error.configure(text=error)
            return

        self.destroy()


class BooksPage(BasePage):
    page_key = "books"
    page_title = "Livres"

    def __init__(self, master, app):
        super().__init__(master, app)
        self._available_only = False
        self._search_by_author = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

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
            command=self.open_add_dialog,
            width=160,
        )
        self.add_button.grid(row=0, column=4, padx=(12, 0))

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

    def _set_feedback(self, text, error=False):
        self.feedback.configure(
            text=text,
            text_color=theme.COLORS["danger"] if error else theme.COLORS["muted"],
        )

    def open_add_dialog(self):
        if self.library is None:
            self._set_feedback("Bibliothèque indisponible.", error=True)
            return
        AddBookDialog(self.app, self.add_book)

    def add_book(self, title, author, isbn):
        try:
            added = self.library.add_book(title, author, isbn)
        except Exception as exc:
            return f"Erreur : {exc}"

        if not added:
            return "Un livre avec cet ISBN existe déjà."

        self._set_feedback("Livre ajouté. La sauvegarde se fera à la fermeture.")
        self.refresh()
        return None

    def confirm_delete(self, book):
        if not book["available"]:
            MessageDialog(
                self.app,
                "Suppression impossible",
                (
                    f"Le livre « {book['title']} » est emprunté par "
                    f"{book['borrower_id']}. Retournez-le avant de le supprimer."
                ),
            )
            return

        ConfirmDialog(
            self.app,
            "Supprimer le livre",
            (
                f"Voulez-vous vraiment supprimer « {book['title']} » "
                f"(ISBN {book['isbn']}) ?"
            ),
            lambda: self.remove_book(book),
        )

    def remove_book(self, book):
        try:
            removed = self.library.remove_book(book["isbn"])
        except Exception as exc:
            self._set_feedback(f"Erreur : {exc}", error=True)
            return

        if not removed:
            self._set_feedback(
                "Suppression impossible : livre introuvable ou emprunté.",
                error=True,
            )
            self.refresh()
            return

        self._set_feedback("Livre supprimé. La sauvegarde se fera à la fermeture.")
        self.refresh()

    def handle_action(self, book):
        if book["available"]:
            self.open_borrow_dialog(book)
        else:
            self.return_book(book)

    def open_borrow_dialog(self, book):
        if self.library is None:
            self._set_feedback("Bibliothèque indisponible.", error=True)
            return

        try:
            users = self.library.list_users()
        except Exception as exc:
            self._set_feedback(f"Erreur de chargement : {exc}", error=True)
            return

        if not users:
            MessageDialog(
                self.app,
                "Aucun utilisateur",
                "Ajoutez d'abord un utilisateur avant d'emprunter un livre.",
            )
            return

        BorrowDialog(
            self.app,
            book,
            users,
            lambda user_id: self.borrow_book(book, user_id),
        )

    def borrow_book(self, book, user_id):
        try:
            borrowed = self.library.checkout(book["isbn"], user_id)
        except Exception as exc:
            return f"Erreur : {exc}"

        if not borrowed:
            self.refresh()
            return (
                "Emprunt impossible : livre ou utilisateur introuvable, "
                "ou livre déjà emprunté."
            )

        self._set_feedback(
            f"Livre emprunté par {user_id}. La sauvegarde se fera à la fermeture."
        )
        self.refresh()
        return None

    def return_book(self, book):
        try:
            returned = self.library.return_book(book["isbn"])
        except Exception as exc:
            self._set_feedback(f"Erreur : {exc}", error=True)
            return

        if not returned:
            self._set_feedback(
                "Retour impossible : livre introuvable ou déjà disponible.",
                error=True,
            )
            self.refresh()
            return

        self._set_feedback("Livre retourné. La sauvegarde se fera à la fermeture.")
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
            BookCard(
                self.scroll,
                book,
                on_delete=lambda b=book: self.confirm_delete(b),
                on_action=lambda b=book: self.handle_action(b),
            ).pack(fill="x", pady=6)
