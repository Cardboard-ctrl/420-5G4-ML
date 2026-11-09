import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    page_key = ""
    page_title = ""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)

    @property
    def library(self):
        return self.app.library

    def on_show(self):
        self.refresh()

    def refresh(self):
        pass
