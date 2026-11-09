import customtkinter as ctk

import theme
from ui import icons


class NavItem(ctk.CTkFrame):
    def __init__(self, master, key, icon_name, command):
        super().__init__(master, fg_color="transparent")
        self.key = key
        self.icon_name = icon_name
        self.command = command

        self.button = ctk.CTkButton(
            self,
            text="",
            image=icons.nav_icon(icon_name, active=False),
            width=64,
            height=42,
            corner_radius=theme.RADIUS["button"],
            fg_color="transparent",
            hover_color=theme.COLORS["surface_alt"],
            command=lambda: self.command(self.key),
        )
        self.button.pack()
        self.underline = ctk.CTkFrame(
            self,
            width=28,
            height=3,
            corner_radius=2,
            fg_color="transparent",
        )
        self.underline.pack(pady=(2, 0))

    def set_active(self, active):
        self.button.configure(image=icons.nav_icon(self.icon_name, active=active))
        self.underline.configure(
            fg_color=theme.COLORS["accent"] if active else "transparent"
        )


class NavBar(ctk.CTkFrame):
    def __init__(self, master, on_change):
        super().__init__(
            master,
            height=70,
            corner_radius=0,
            fg_color=theme.COLORS["nav"],
            border_width=1,
            border_color=theme.COLORS["border"],
        )
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        for column in range(3):
            self.grid_columnconfigure(column, weight=1)

        entries = [
            ("users", "users"),
            ("books", "books"),
            ("settings", "gear"),
        ]
        self.items = {}
        for column, (key, icon_name) in enumerate(entries):
            item = NavItem(self, key, icon_name, on_change)
            item.grid(row=0, column=column, sticky="nsew")
            self.items[key] = item

    def set_active(self, key):
        for item_key, item in self.items.items():
            item.set_active(item_key == key)
