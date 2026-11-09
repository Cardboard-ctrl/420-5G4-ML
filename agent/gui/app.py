import customtkinter as ctk


class SmokeTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Test customtkinter - Bibliothèque")
        self.geometry("480x360")
        self.minsize(400, 300)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.status_text = ctk.StringVar(value="customtkinter est prêt")
        self.click_count = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Test de fonctionnement de customtkinter",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, padx=24, pady=(24, 12), sticky="ew")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=24, pady=12, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.content_frame,
            textvariable=self.status_text,
            font=ctk.CTkFont(size=15),
        )
        self.status_label.grid(row=0, column=0, padx=16, pady=(24, 16))

        self.theme_button = ctk.CTkButton(
            self.content_frame,
            text="Changer le thème",
            command=self.toggle_theme,
        )
        self.theme_button.grid(row=1, column=0, padx=16, pady=8)

        self.counter_label = ctk.CTkLabel(
            self.content_frame,
            text="Clics : 0",
            font=ctk.CTkFont(size=15),
        )
        self.counter_label.grid(row=2, column=0, padx=16, pady=(16, 8))

        self.counter_button = ctk.CTkButton(
            self.content_frame,
            text="Compter un clic",
            command=self.increment_counter,
        )
        self.counter_button.grid(row=3, column=0, padx=16, pady=8)

        self.quit_button = ctk.CTkButton(
            self.content_frame,
            text="Quitter",
            command=self.destroy,
            fg_color="#b3261e",
            hover_color="#8c1d18",
        )
        self.quit_button.grid(row=4, column=0, padx=16, pady=(16, 16))

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.status_text.set("Mode clair activé")
        else:
            ctk.set_appearance_mode("Dark")
            self.status_text.set("Mode sombre activé")

    def increment_counter(self):
        self.click_count += 1
        self.counter_label.configure(text=f"Clics : {self.click_count}")


if __name__ == "__main__":
    app = SmokeTestApp()
    app.mainloop()
