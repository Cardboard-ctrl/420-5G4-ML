import io
from functools import lru_cache
from pathlib import Path

import customtkinter as ctk

try:
    import resvg_py
except ImportError:
    resvg_py = None

try:
    from PIL import Image, ImageColor
except ImportError:
    Image = None
    ImageColor = None

from theme import color

ICON_DIR = Path(__file__).resolve().parent.parent / "icons"

ICON_FILES = {
    "books": "books-svgrepo-com.svg",
    "add_book": "education-book-add-svgrepo-com.svg",
    "gear": "gear-svgrepo-com.svg",
    "moon": "moon-svgrepo-com.svg",
    "save": "save-svgrepo-com.svg",
    "search": "search-svgrepo-com.svg",
    "stats": "stats-1367-svgrepo-com.svg",
    "swap": "swap-svgrepo-com.svg",
    "trash": "trash-svgrepo-com.svg",
    "user_plus": "user-plus-alt-1-svgrepo-com.svg",
    "users": "users-svgrepo-com.svg",
}

SCALE = 3
_ctk_cache = {}


def available():
    return resvg_py is not None and Image is not None


def _icon_path(name):
    filename = ICON_FILES.get(name)
    if filename is None:
        raise KeyError(f"Icone inconnue: {name}")
    path = ICON_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


@lru_cache(maxsize=None)
def _alpha_mask(name, size):
    path = _icon_path(name)
    png = resvg_py.svg_to_bytes(svg_path=str(path), width=size, height=size)
    with Image.open(io.BytesIO(png)) as image:
        return image.convert("RGBA").getchannel("A")


def _tint(name, size, hex_color, opacity):
    alpha = _alpha_mask(name, size)
    if opacity < 255:
        alpha = alpha.point(lambda value: value * opacity // 255)
    red, green, blue = ImageColor.getrgb(hex_color)
    image = Image.new("RGBA", (size, size), (red, green, blue, 255))
    image.putalpha(alpha)
    return image


def render_icon(name, size=24, hex_color="#000000", opacity=255):
    if not available():
        return None
    return _tint(name, size * SCALE, hex_color, opacity)


def icon(name, size=24, color_key="text", opacity=255, disabled=False):
    if not available():
        return None

    if disabled:
        opacity = min(opacity, 120)

    light = color(color_key, "Light")
    dark = color(color_key, "Dark")
    cache_key = (name, size, light, dark, opacity)

    if cache_key not in _ctk_cache:
        light_image = _tint(name, size * SCALE, light, opacity)
        dark_image = _tint(name, size * SCALE, dark, opacity)
        _ctk_cache[cache_key] = ctk.CTkImage(
            light_image=light_image,
            dark_image=dark_image,
            size=(size, size),
        )

    return _ctk_cache[cache_key]


def nav_icon(name, active=False, size=30):
    return icon(name, size, "accent" if active else "text")
