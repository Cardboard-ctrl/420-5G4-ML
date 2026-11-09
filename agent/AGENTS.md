# AGENTS.md

Scope: only the `agent/` project (C++ app + optional Python GUI). The Python notebooks elsewhere in the repo are out of scope.
`agent/README.md` has the minimal build steps; this file records the non-obvious details.

## Build and run
From this directory:
```bash
cmake -S . -B build && cmake --build build
./build/bibliotheque -d data
```
- Targets: `biblio_core` (static lib: book/user/library/filemanager), `bibliotheque` (CLI, `main.cpp`), optional `bibliotheque_py` (pybind11 module).
- `-d/--data-dir` is effectively required. Without it the data-file paths stay empty: nothing loads and saves fail. Use `-d data` for the sample files here.
- `build/` contents are gitignored (`.gitignore` has `build/*`).
- Sources are listed explicitly (no `file(GLOB)`): add new `.cpp` files to the matching target in `CMakeLists.txt`.
- C++17, warnings `-Wall -Wextra -Wpedantic`. No lint, formatter, or CI. Bridge tests: `python3 tests/test_bridge.py`.
- `biblio_core` must stay `POSITION_INDEPENDENT_CODE ON`; otherwise the pybind module fails to link (`recompile with -fPIC`).

## Python bridge (pybind11)
- Module is `bibliotheque_py`, built to `build/`; import with `PYTHONPATH=build` or via `gui/bibliotheque_api.py`.
- Build on/off: `cmake -S . -B build -DBUILD_PYTHON_BINDINGS=ON|OFF`.
- Bindings live in `bindings/bindings.cpp` (not in `biblio_core`). `display*` methods are intentionally not exposed.
- Raw `Book*`/`User*` returns MUST use `py::return_value_policy::reference_internal`: `Library` owns them via `unique_ptr`, and pybind's default `take_ownership` double-frees.
- The extension ABI is tied to the Python found by CMake (currently `/usr/bin/python3` 3.13). For `gui/.venv`, configure with `-DPYTHON_EXECUTABLE=gui/.venv/bin/python` (this Debian pybind11 uses the uppercase legacy variable, not `Python_EXECUTABLE`).
- `gui/bibliotheque_api.py` is the stable Python facade; it converts C++ objects to plain dicts so GUI code does not depend on C++ lifetimes.

## Data files
`data/books.txt` and `data/users.txt` are pipe-separated; avoid `|` inside fields.
- book: `title|author|isbn|available|borrowerId`, where `available` is `1` or `0`
- user: `name|userId|isbn1,isbn2,...`
Data loads at startup. Menu 12 saves both files; menu 0 saves before exit. Menu 13 copies the current on-disk files to `.backup` but does not save unsaved in-memory changes first.

## Code structure
- `main.cpp` is only the interactive menu; all user-facing strings are French.
- `Library` owns books/users with `unique_ptr`. Methods returning `Book*`/`User*` are non-owning; do not delete them.
- `Book`/`User` own their `toFileFormat`/`fromFileFormat` logic; `FileManager` reads/writes whole collections.
- Headers use include guards and put `using namespace std;` in headers, matching existing style.

## GUI (`gui/`)
Minimal customtkinter smoke test. Use the GUI-specific venv, not the repo-root one. `gui/bibliotheque_api.py` provides the bridge facade (`Bibliotheque.open(data_dir)`, dict-returning methods); `app.py` itself is still standalone.
```bash
cd gui
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```
- Requires an X11 display (this shell has `DISPLAY=:0`; the devcontainer mounts `/tmp/.X11-unix`).
- `customtkinter` is pinned in `gui/requirements.txt`; `.venv/` is gitignored by the root `.gitignore`.
- Manual check: window opens, theme button toggles light/dark, counter increments, Quit closes.

## Devcontainer
`.devcontainer/` is optional. It mounts X11 (`/tmp/.X11-unix`), uses host networking, and installs CMake, Ollama, and opencode.
