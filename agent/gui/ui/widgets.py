import customtkinter as ctk

import theme
from ui import icons
from ui.table import ACTION_PAD_RIGHT, TableCard


class IconButton(ctk.CTkButton):
    def __init__(
        self,
        master,
        icon_name,
        command=None,
        size=18,
        color_key="text",
        disabled=False,
        **kwargs,
    ):
        image = icons.icon(icon_name, size, color_key, disabled=disabled)
        fallback = "" if image is not None else icon_name.replace("_", " ").title()
        options = {
            "text": fallback,
            "image": image,
            "width": size + 18,
            "height": size + 18,
            "corner_radius": theme.RADIUS["button"],
            "fg_color": "transparent",
            "hover_color": theme.COLORS["surface_alt"],
            "text_color": theme.COLORS["text"],
            "command": command,
            "state": "disabled" if disabled else "normal",
        }
        options.update(kwargs)
        super().__init__(master, **options)


class IconTextButton(ctk.CTkButton):
    def __init__(
        self,
        master,
        icon_name,
        text,
        command=None,
        icon_size=18,
        color_key="text",
        disabled=False,
        **kwargs,
    ):
        image = icons.icon(icon_name, icon_size, color_key, disabled=disabled)
        options = {
            "text": text,
            "image": image,
            "compound": "left",
            "height": 34,
            "corner_radius": theme.RADIUS["button"],
            "fg_color": theme.COLORS["button"],
            "hover_color": theme.COLORS["button_hover"],
            "text_color": theme.COLORS["text"],
            "font": theme.small_font(),
            "command": command,
            "state": "disabled" if disabled else "normal",
        }
        options.update(kwargs)
        super().__init__(master, **options)


class SearchBar(ctk.CTkFrame):
    def __init__(self, master, placeholder, command=None, **kwargs):
        super().__init__(
            master,
            corner_radius=theme.RADIUS["pill"],
            fg_color=theme.COLORS["surface_alt"],
            **kwargs,
        )
        self.command = command
        self.entry = ctk.CTkEntry(
            self,
            height=34,
            border_width=0,
            fg_color="transparent",
            text_color=theme.COLORS["text"],
            placeholder_text_color=theme.COLORS["muted"],
            placeholder_text=placeholder,
            font=theme.body_font(),
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(18, 4), pady=5)
        self.icon_label = ctk.CTkLabel(
            self,
            text="",
            image=icons.icon("search", 18, "muted"),
        )
        self.icon_label.pack(side="right", padx=(4, 16))
        self.entry.bind("<KeyRelease>", self._notify)
        self.entry.bind("<Return>", self._notify)

    def _notify(self, _event=None):
        if self.command is not None:
            self.command()

    def get(self):
        return self.entry.get().strip()

    def set_placeholder(self, text):
        self.entry.configure(placeholder_text=text)


class IconTile(ctk.CTkFrame):
    def __init__(self, master, icon_name, text, command=None, icon_size=54):
        super().__init__(master, fg_color="transparent")
        self.command = command
        self.panel = ctk.CTkButton(
            self,
            text="",
            image=icons.icon(icon_name, icon_size, "text"),
            width=132,
            height=100,
            corner_radius=theme.RADIUS["card"],
            fg_color=theme.COLORS["surface_alt"],
            hover_color=theme.COLORS["button"],
            command=self._invoke,
        )
        self.panel.pack()
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=theme.small_font(),
            text_color=theme.COLORS["text"],
            wraplength=190,
            justify="center",
            cursor="hand2",
        )
        self.label.pack(pady=(10, 0))
        self.label.bind("<Button-1>", lambda _event: self._invoke())

    def _invoke(self):
        if self.command is not None:
            self.command()


class BookCard(TableCard):
    def __init__(self, master, book, on_delete=None, on_action=None):
        status = (
            "Disponible"
            if book["available"]
            else f"Emprunté par : {book['borrower_id']}"
        )
        action_text = "Emprunter" if book["available"] else "Retourner"
        super().__init__(
            master,
            (
                ("Titre", book["title"]),
                ("Auteur", book["author"]),
                ("ISBN", book["isbn"]),
                ("Status", status),
            ),
        )
        self.book = book

        IconButton(
            self.action_rail,
            "trash",
            command=on_delete,
            size=18,
            disabled=on_delete is None,
        ).pack(anchor="e", padx=(0, ACTION_PAD_RIGHT), pady=(10, 0))
        ctk.CTkButton(
            self.action_rail,
            text=action_text,
            command=on_action,
            state="normal" if on_action is not None else "disabled",
            width=112,
            height=30,
            font=theme.small_font(),
            corner_radius=theme.RADIUS["button"],
            fg_color=theme.COLORS["button"],
            hover_color=theme.COLORS["button_hover"],
            text_color=theme.COLORS["text"],
            text_color_disabled=theme.COLORS["muted"],
        ).pack(anchor="e", padx=(0, ACTION_PAD_RIGHT), pady=(8, 0))


class UserCard(TableCard):
    def __init__(self, master, user):
        borrowed = user["borrowed_books"]
        isbns = ", ".join(borrowed) if borrowed else "N/A"
        super().__init__(
            master,
            (
                ("ID", user["user_id"]),
                ("Nom", user["name"]),
                ("Livres empruntés", str(len(borrowed))),
                ("ISBNs", isbns),
            ),
            with_actions=False,
        )
        self.user = user


class EmptyState(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(
            master,
            text=text,
            font=theme.body_font(),
            text_color=theme.COLORS["muted"],
            pady=24,
        )
