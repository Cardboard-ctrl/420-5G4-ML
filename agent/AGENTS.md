# AGENTS.md

Scope: only the `agent/` C++ project. The Python notebooks elsewhere in the repo are out of scope.
`agent/README.md` has the minimal build steps; this file records the non-obvious details.

## Build and run
From this directory:
```bash
cmake -S . -B build && cmake --build build
./build/bibliotheque -d data
```
- Executable is `bibliotheque` (`add_executable(${PROJECT_NAME} ...)`).
- `-d/--data-dir` is effectively required. Without it the data-file paths stay empty: nothing loads and saves fail. Use `-d data` for the sample files here.
- `build/` contents are gitignored (`.gitignore` has `build/*`).
- `CMakeLists.txt` uses `file(GLOB "*.cpp")` without `CONFIGURE_DEPENDS`: re-run cmake after adding or removing a `.cpp` file.
- C++17, warnings `-Wall -Wextra -Wpedantic`. No tests, lint, formatter, or CI.

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

## Devcontainer
`.devcontainer/` is optional. It mounts X11 (`/tmp/.X11-unix`), uses host networking, and installs CMake, Ollama, and opencode.
