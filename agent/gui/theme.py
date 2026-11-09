import customtkinter as ctk

COLORS = {
    "window": ("#D8E2FF", "#1B2232"),
    "surface": ("#C9D4F3", "#2A3348"),
    "surface_alt": ("#E6ECFF", "#242D40"),
    "nav": ("#E7EDFF", "#222A3C"),
    "border": ("#B7C3E5", "#3B4763"),
    "text": ("#1B1B1F", "#F2F4FF"),
    "muted": ("#62677A", "#AAB3C8"),
    "accent": ("#4F6BED", "#8FA8FF"),
    "button": ("#BFCBEF", "#33415F"),
    "button_hover": ("#AFBDE8", "#3D4D70"),
    "danger": ("#B3261E", "#E06C63"),
}

RADIUS = {
    "window": 0,
    "card": 12,
    "button": 8,
    "pill": 22,
}


def color(key, mode=None):
    value = COLORS[key]
    if not isinstance(value, tuple):
        return value
    if mode is None:
        mode = ctk.get_appearance_mode()
    return value[0] if mode.lower() == "light" else value[1]


def font(size, weight="normal"):
    return ctk.CTkFont(size=size, weight=weight)


def title_font():
    return font(32, "bold")


def subtitle_font():
    return font(14)


def body_font():
    return font(15)


def small_font():
    return font(13)


def toggled_mode():
    return "Dark" if ctk.get_appearance_mode().lower() == "light" else "Light"
