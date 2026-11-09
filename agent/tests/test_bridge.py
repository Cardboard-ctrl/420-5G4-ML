import shutil
import sys
import tempfile
import unittest
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_AGENT_ROOT / "gui"))

from bibliotheque_api import Bibliotheque, BibliothequeError


class BridgeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self._tmp.name)
        shutil.copytree(_AGENT_ROOT / "data", self.data_dir, dirs_exist_ok=True)
        self.expected_books = self._count_lines(self.data_dir / "books.txt")
        self.expected_users = self._count_lines(self.data_dir / "users.txt")
        self.biblio = Bibliotheque(self.data_dir)

    def tearDown(self):
        del self.biblio
        self._tmp.cleanup()

    @staticmethod
    def _count_lines(path):
        return len([line for line in path.read_text(encoding="utf-8").splitlines() if line])

    def test_load_counts(self):
        self.assertEqual(len(self.biblio.list_books()), self.expected_books)
        self.assertEqual(len(self.biblio.list_users()), self.expected_users)

    def test_iterate_all_fields(self):
        for book in self.biblio.list_books():
            self.assertIn("title", book)
            self.assertIn("author", book)
            self.assertIn("isbn", book)
            self.assertIsInstance(book["available"], bool)
            self.assertIsInstance(book["borrower_id"], str)
        for user in self.biblio.list_users():
            self.assertIn("name", user)
            self.assertIn("user_id", user)
            self.assertIsInstance(user["borrowed_books"], list)

    def test_add_checkout_return_save_reload(self):
        self.assertTrue(self.biblio.add_book("Titre Test", "Auteur Test", "9780000000001"))
        self.assertTrue(self.biblio.add_user("Utilisateur Test", "USR-TEST"))
        self.assertFalse(self.biblio.add_book("Doublon", "Auteur", "9780000000001"))
        self.assertFalse(self.biblio.add_user("Doublon", "USR-TEST"))

        self.assertTrue(self.biblio.checkout("9780000000001", "USR-TEST"))
        book = self.biblio.get_book("9780000000001")
        self.assertFalse(book["available"])
        self.assertEqual(book["borrower_id"], "USR-TEST")
        user = self.biblio.get_user("USR-TEST")
        self.assertIn("9780000000001", user["borrowed_books"])

        self.assertTrue(self.biblio.save())
        self.assertTrue(self.biblio.return_book("9780000000001"))
        self.assertTrue(self.biblio.get_book("9780000000001")["available"])

        reloaded = Bibliotheque(self.data_dir)
        self.assertIsNotNone(reloaded.get_book("9780000000001"))
        self.assertIsNotNone(reloaded.get_user("USR-TEST"))
        self.assertEqual(len(reloaded.list_books()), self.expected_books + 1)

    def test_checkout_guards(self):
        available = next(
            book for book in self.biblio.list_books() if book["available"]
        )
        user = self.biblio.list_users()[0]

        self.assertFalse(self.biblio.checkout("9780000000009", user["user_id"]))
        self.assertFalse(self.biblio.checkout(available["isbn"], "USR-UNKNOWN"))
        self.assertTrue(self.biblio.checkout(available["isbn"], user["user_id"]))
        self.assertFalse(self.biblio.checkout(available["isbn"], user["user_id"]))

        book = self.biblio.get_book(available["isbn"])
        self.assertFalse(book["available"])
        self.assertEqual(book["borrower_id"], user["user_id"])
        self.assertIn(
            available["isbn"],
            self.biblio.get_user(user["user_id"])["borrowed_books"],
        )

        self.assertTrue(self.biblio.return_book(available["isbn"]))
        self.assertFalse(self.biblio.return_book(available["isbn"]))

        book = self.biblio.get_book(available["isbn"])
        self.assertTrue(book["available"])
        self.assertEqual(book["borrower_id"], "")
        self.assertNotIn(
            available["isbn"],
            self.biblio.get_user(user["user_id"])["borrowed_books"],
        )

    def test_remove_book(self):
        available = next(
            book for book in self.biblio.list_books() if book["available"]
        )
        self.assertTrue(self.biblio.remove_book(available["isbn"]))
        self.assertIsNone(self.biblio.get_book(available["isbn"]))
        self.assertFalse(self.biblio.remove_book(available["isbn"]))

        borrowed = next(
            book for book in self.biblio.list_books() if not book["available"]
        )
        self.assertFalse(self.biblio.remove_book(borrowed["isbn"]))
        self.assertTrue(self.biblio.return_book(borrowed["isbn"]))
        self.assertTrue(self.biblio.remove_book(borrowed["isbn"]))

    def test_search(self):
        first = self.biblio.list_books()[0]
        self.assertTrue(self.biblio.search_by_title(first["title"].lower()))
        self.assertTrue(self.biblio.search_by_author(first["author"].lower()))
        self.assertEqual(self.biblio.search_by_title("introuvable-xyz"), [])

    def test_stats(self):
        stats = self.biblio.stats()
        self.assertEqual(stats["total_books"], self.expected_books)
        self.assertEqual(
            stats["total_books"],
            stats["available_books"] + stats["checked_out_books"],
        )
        self.assertEqual(stats["total_users"], self.expected_users)

    def test_missing_dir(self):
        with self.assertRaises(BibliothequeError):
            Bibliotheque(self.data_dir / "absent")


if __name__ == "__main__":
    unittest.main()
