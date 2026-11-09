# Construire le projet
Vous pouvez utiliser un dev container de base C++ de VScode.
Le projet utilise cmake, pensez à l'inclure dans votre dev container.

Voici les lignes de commandes pour compiler le projet:
```
$ mkdir build
$ cd build
$ cmake ..
$ make
```

# Répertoire data

Il contient 2 fichiers `books.txt`et `users.txt` que vous pouvez utilisez pour tester votre code.
Pour ca il suffit de donner chemin vers le repertoire data avec l'application `bibliotheque -d <chemin verrs data>`

# Liaison Python (pybind11)

Le module `bibliotheque_py` expose `Book`, `User`, `Library` et `FileManager`.
La compilation se fait avec le projet:

```
$ cmake -S . -B build -DBUILD_PYTHON_BINDINGS=ON
$ cmake --build build
```

Puis, depuis le repertoire `agent/`:

```
$ PYTHONPATH=build python3 -c "import bibliotheque_py"
$ python3 tests/test_bridge.py
```

Le module est ecrit dans `build/`. La facade `gui/bibliotheque_api.py` fournit une API Python simple (`Bibliotheque.open(data_dir)`, methodes renvoyant des dictionnaires).

# Interface graphique (CustomTkinter)

L'application se trouve dans `gui/` et utilise un environnement virtuel dedie:

```
$ cd gui
$ python3 -m venv .venv
$ .venv/bin/python -m pip install -r requirements.txt
$ .venv/bin/python app.py -d ../data
```

Les icones SVG sont dans `gui/icons/` et sont converties en images par `resvg_py`, puis teintees avec Pillow selon le theme clair/sombre. Les tests des icones se lancent avec:

```
$ .venv/bin/python -m unittest discover -s tests
```