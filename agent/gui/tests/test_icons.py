import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ui import icons


def first_visible_pixel(image):
    alpha = image.getchannel("A")
    width, height = image.size
    for y in range(height):
        for x in range(width):
            if alpha.getpixel((x, y)) > 0:
                return image.getpixel((x, y))
    return None


class IconTest(unittest.TestCase):
    def test_dependencies_available(self):
        self.assertTrue(icons.available())

    def test_all_icons_render(self):
        for name in icons.ICON_FILES:
            with self.subTest(name=name):
                image = icons.render_icon(name, 24, "#000000")
                self.assertEqual(image.size, (24 * icons.SCALE, 24 * icons.SCALE))
                self.assertIsNotNone(first_visible_pixel(image))

    def test_tint_changes_visible_pixels(self):
        black = icons.render_icon("books", 16, "#000000")
        white = icons.render_icon("books", 16, "#FFFFFF")
        self.assertNotEqual(
            first_visible_pixel(black),
            first_visible_pixel(white),
        )

    def test_unknown_icon(self):
        with self.assertRaises(KeyError):
            icons.render_icon("unknown", 16, "#000000")


if __name__ == "__main__":
    unittest.main()
