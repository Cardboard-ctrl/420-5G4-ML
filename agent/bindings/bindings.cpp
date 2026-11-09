#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <string>

#include "book.h"
#include "user.h"
#include "library.h"
#include "filemanager.h"

namespace py = pybind11;

PYBIND11_MODULE(bibliotheque_py, m) {
    m.doc() = "Liaison Python du systeme de gestion de bibliotheque personnelle";

    py::class_<Book>(m, "Book")
        .def(py::init<>())
        .def(py::init<const std::string&, const std::string&, const std::string&>(),
             py::arg("title"), py::arg("author"), py::arg("isbn"))
        .def("getTitle", &Book::getTitle)
        .def("getAuthor", &Book::getAuthor)
        .def("getISBN", &Book::getISBN)
        .def("getAvailability", &Book::getAvailability)
        .def("getBorrowerId", &Book::getBorrowerId)
        .def("setTitle", &Book::setTitle, py::arg("title"))
        .def("setAuthor", &Book::setAuthor, py::arg("author"))
        .def("setISBN", &Book::setISBN, py::arg("isbn"))
        .def("setAvailability", &Book::setAvailability, py::arg("available"))
        .def("setBorrowerId", &Book::setBorrowerId, py::arg("id"))
        .def("checkOut", &Book::checkOut, py::arg("borrowerId"))
        .def("returnBook", &Book::returnBook)
        .def("toString", &Book::toString)
        .def("toFileFormat", &Book::toFileFormat)
        .def("fromFileFormat", &Book::fromFileFormat, py::arg("line"));

    py::class_<User>(m, "User")
        .def(py::init<>())
        .def(py::init<const std::string&, const std::string&>(),
             py::arg("name"), py::arg("userId"))
        .def("getName", &User::getName)
        .def("getUserId", &User::getUserId)
        .def("getBorrowedBooks", &User::getBorrowedBooks)
        .def("setName", &User::setName, py::arg("name"))
        .def("setUserId", &User::setUserId, py::arg("userId"))
        .def("borrowBook", &User::borrowBook, py::arg("isbn"))
        .def("returnBook", &User::returnBook, py::arg("isbn"))
        .def("hasBorrowedBook", &User::hasBorrowedBook, py::arg("isbn"))
        .def("getNumberOfBorrowedBooks", &User::getNumberOfBorrowedBooks)
        .def("toString", &User::toString)
        .def("toFileFormat", &User::toFileFormat)
        .def("fromFileFormat", &User::fromFileFormat, py::arg("line"));

    py::class_<Library>(m, "Library")
        .def(py::init<>())
        .def("addBook", &Library::addBook, py::arg("book"))
        .def("removeBook", &Library::removeBook, py::arg("isbn"))
        .def("findBookByISBN", &Library::findBookByISBN, py::arg("isbn"),
             py::return_value_policy::reference_internal)
        .def("searchBooksByTitle", &Library::searchBooksByTitle, py::arg("title"),
             py::return_value_policy::reference_internal)
        .def("searchBooksByAuthor", &Library::searchBooksByAuthor, py::arg("author"),
             py::return_value_policy::reference_internal)
        .def("getAvailableBooks", &Library::getAvailableBooks,
             py::return_value_policy::reference_internal)
        .def("getAllBooks", &Library::getAllBooks,
             py::return_value_policy::reference_internal)
        .def("addUser", &Library::addUser, py::arg("user"))
        .def("findUserById", &Library::findUserById, py::arg("userId"),
             py::return_value_policy::reference_internal)
        .def("getAllUsers", &Library::getAllUsers,
             py::return_value_policy::reference_internal)
        .def("checkOutBook", &Library::checkOutBook, py::arg("isbn"), py::arg("userId"))
        .def("returnBook", &Library::returnBook, py::arg("isbn"))
        .def("getTotalBooks", &Library::getTotalBooks)
        .def("getAvailableBookCount", &Library::getAvailableBookCount)
        .def("getCheckedOutBookCount", &Library::getCheckedOutBookCount);

    py::class_<FileManager>(m, "FileManager")
        .def(py::init<const std::string&, const std::string&>(),
             py::arg("booksFile"), py::arg("usersFile"))
        .def("saveLibraryData", &FileManager::saveLibraryData, py::arg("library"))
        .def("loadLibraryData", &FileManager::loadLibraryData, py::arg("library"))
        .def("saveBooksToFile", &FileManager::saveBooksToFile, py::arg("library"))
        .def("saveUsersToFile", &FileManager::saveUsersToFile, py::arg("library"))
        .def("loadBooksFromFile", &FileManager::loadBooksFromFile, py::arg("library"))
        .def("loadUsersFromFile", &FileManager::loadUsersFromFile, py::arg("library"))
        .def("fileExists", &FileManager::fileExists, py::arg("filename"))
        .def("createBackup", &FileManager::createBackup);

    m.def("make_file_manager", [](const std::string& dataDir) {
        return FileManager(dataDir + "/books.txt", dataDir + "/users.txt");
    }, py::arg("dataDir"),
       "Cree un FileManager a partir d'un repertoire data (books.txt, users.txt)");
}
