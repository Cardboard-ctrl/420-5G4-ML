import os
import sys
from pathlib import Path

_AGENT_ROOT = Path(__file__).resolve().parent.parent
_BUILD_DIR = Path(os.environ.get("BIBLIOTHEQUE_BUILD_DIR", _AGENT_ROOT / "build"))
if str(_BUILD_DIR) not in sys.path:
    sys.path.insert(0, str(_BUILD_DIR))

import bibliotheque_py

__all__ = ["Bibliotheque", "BibliothequeError"]


class BibliothequeError(Exception):
    pass


def _book_to_dict(book):
    return {
        "title": book.getTitle(),
        "author": book.getAuthor(),
        "isbn": book.getISBN(),
        "available": book.getAvailability(),
        "borrower_id": book.getBorrowerId(),
    }


def _user_to_dict(user):
    return {
        "name": user.getName(),
        "user_id": user.getUserId(),
        "borrowed_books": list(user.getBorrowedBooks()),
    }


class Bibliotheque:
    def __init__(self, data_dir=None):
        self._library = None
        self._file_manager = None
        if data_dir is not None:
            self.open(data_dir)

    def open(self, data_dir):
        data_dir = str(data_dir)
        self._data_dir = data_dir
        if not os.path.isdir(data_dir):
            raise BibliothequeError(f"Repertoire introuvable: {data_dir}")
        self._library = bibliotheque_py.Library()
        self._file_manager = bibliotheque_py.make_file_manager(data_dir)
        self._file_manager.loadLibraryData(self._library)
        return self

    def _require_open(self):
        if self._library is None:
            raise BibliothequeError("Aucune bibliotheque ouverte")

    def save(self):
        self._require_open()
        return bool(self._file_manager.saveLibraryData(self._library))

    def create_backup(self):
        self._require_open()
        self._file_manager.createBackup()

    def list_books(self, available_only=False):
        self._require_open()
        books = (
            self._library.getAvailableBooks()
            if available_only
            else self._library.getAllBooks()
        )
        return [_book_to_dict(book) for book in books]

    def get_book(self, isbn):
        self._require_open()
        book = self._library.findBookByISBN(isbn)
        return None if book is None else _book_to_dict(book)

    def list_users(self):
        self._require_open()
        return [_user_to_dict(user) for user in self._library.getAllUsers()]

    def get_user(self, user_id):
        self._require_open()
        user = self._library.findUserById(user_id)
        return None if user is None else _user_to_dict(user)

    def add_book(self, title, author, isbn):
        self._require_open()
        if self._library.findBookByISBN(isbn) is not None:
            return False
        self._library.addBook(bibliotheque_py.Book(title, author, isbn))
        return True

    def remove_book(self, isbn):
        self._require_open()
        book = self._library.findBookByISBN(isbn)
        if book is None or not book.getAvailability():
            return False
        return bool(self._library.removeBook(isbn))

    def search_by_title(self, title):
        self._require_open()
        return [_book_to_dict(book) for book in self._library.searchBooksByTitle(title)]

    def search_by_author(self, author):
        self._require_open()
        return [_book_to_dict(book) for book in self._library.searchBooksByAuthor(author)]

    def add_user(self, name, user_id):
        self._require_open()
        if self._library.findUserById(user_id) is not None:
            return False
        self._library.addUser(bibliotheque_py.User(name, user_id))
        return True

    def checkout(self, isbn, user_id):
        self._require_open()
        return bool(self._library.checkOutBook(isbn, user_id))

    def return_book(self, isbn):
        self._require_open()
        return bool(self._library.returnBook(isbn))

    def stats(self):
        self._require_open()
        return {
            "total_books": self._library.getTotalBooks(),
            "available_books": self._library.getAvailableBookCount(),
            "checked_out_books": self._library.getCheckedOutBookCount(),
            "total_users": len(self._library.getAllUsers()),
        }
