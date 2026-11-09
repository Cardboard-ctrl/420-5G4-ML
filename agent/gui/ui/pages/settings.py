import customtkinter as ctk

import theme
from ui.pages.base import BasePage
from ui.widgets import IconTile


class StatsDialog(ctk.CTkToplevel):
    def __init__(self, master, stats):
        super().__init__(master, fg_color=theme.COLORS["window"])
        self.title("Statistiques de la bibliothèque")
        self.geometry("380x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        content = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS["surface"],
            corner_radius=theme.RADIUS["card"],
        )
        content.pack(fill="both", expand=True, padx=24, pady=24)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            content,
            text="Statistiques de la bibliothèque",
            font=theme.font(18, "bold"),
            text_color=theme.COLORS["text"],
        ).grid(row=0, column=0, pady=(20, 14), padx=20)

        rows = [
            ("Livres au total", stats["total_books"]),
            ("Livres disponibles", stats["available_books"]),
            ("Livres empruntés", stats["checked_out_books"]),
            ("Utilisateurs", stats["total_users"]),
        ]
        for index, (label, value) in enumerate(rows, start=1):
            row = ctk.CTkFrame(content, fg_color="transparent")
            row.grid(row=index, column=0, sticky="ew", padx=24, pady=3)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=label,
                font=theme.body_font(),
                text_color=theme.COLORS["text"],
                anchor="w",
            ).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(
                row,
                text=str(value),
                font=theme.font(15, "bold"),
                text_color=theme.COLORS["accent"],
                anchor="e",
            ).grid(row=0, column=1, sticky="e")

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
        ).grid(row=len(rows) + 1, column=0, pady=(16, 20))


class SettingsPage(BasePage):
    page_key = "settings"
    page_title = "Paramètres"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.save_tile = IconTile(
            self,
            "save",
            "Sauvegarder les données",
            command=self.save_data,
        )
        self.save_tile.grid(row=0, column=0, padx=24, pady=14)

        self.theme_tile = IconTile(
            self,
            "moon",
            "Thème clair/sombre",
            command=self.toggle_theme,
        )
        self.theme_tile.grid(row=0, column=1, padx=24, pady=14)

        self.backup_tile = IconTile(
            self,
            "save",
            "Créer une sauvegarde",
            command=self.create_backup,
        )
        self.backup_tile.grid(row=1, column=0, padx=24, pady=14)

        self.stats_tile = IconTile(
            self,
            "stats",
            "Statistiques de la Bibliothèque",
            command=self.show_stats,
        )
        self.stats_tile.grid(row=1, column=1, padx=24, pady=14)

        self.feedback = ctk.CTkLabel(
            self,
            text="",
            font=theme.body_font(),
            text_color=theme.COLORS["muted"],
        )
        self.feedback.grid(row=2, column=0, columnspan=2, pady=(0, 12))

    def _set_feedback(self, text, error=False):
        self.feedback.configure(
            text=text,
            text_color=theme.COLORS["danger"] if error else theme.COLORS["muted"],
        )

    def save_data(self):
        if self.library is None:
            self._set_feedback("Bibliothèque indisponible.", error=True)
            return
        try:
            ok = self.library.save()
        except Exception as exc:
            self._set_feedback(f"Échec de la sauvegarde : {exc}", error=True)
            return
        if ok:
            self._set_feedback("Données sauvegardées.")
        else:
            self._set_feedback("Échec de la sauvegarde.", error=True)

    def create_backup(self):
        if self.library is None:
            self._set_feedback("Bibliothèque indisponible.", error=True)
            return
        try:
            self.library.create_backup()
        except Exception as exc:
            self._set_feedback(f"Échec de la sauvegarde : {exc}", error=True)
            return
        self._set_feedback("Sauvegarde créée.")

    def toggle_theme(self):
        ctk.set_appearance_mode(theme.toggled_mode())
        self._set_feedback(f"Mode {ctk.get_appearance_mode().lower()} activé.")

    def show_stats(self):
        if self.library is None:
            self._set_feedback("Bibliothèque indisponible.", error=True)
            return
        try:
            stats = self.library.stats()
        except Exception as exc:
            self._set_feedback(f"Erreur : {exc}", error=True)
            return
        StatsDialog(self.app, stats)
