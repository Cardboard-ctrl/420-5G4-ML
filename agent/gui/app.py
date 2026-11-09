import argparse
import os
from pathlib import Path

from ui.shell import BibliothequeApp

AGENT_ROOT = Path(__file__).resolve().parent.parent


def default_data_dir():
    return Path(os.environ.get("BIBLIOTHEQUE_DATA_DIR", AGENT_ROOT / "data"))


def parse_args():
    parser = argparse.ArgumentParser(description="Interface graphique de la bibliothèque")
    parser.add_argument(
        "-d",
        "--data-dir",
        default=str(default_data_dir()),
        help="Répertoire contenant books.txt et users.txt",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    app = BibliothequeApp(Path(args.data_dir))
    app.mainloop()


if __name__ == "__main__":
    main()
