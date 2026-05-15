from pathlib import Path


class Paths:
    ROOT_DIR = Path(__file__).parent.parent.parent
    """ / """

    MIGRATIONS_DIR = ROOT_DIR / "migrations"
    """ /migrations/ """

    ENV_FILE = ROOT_DIR / ".env"
    """ /.env """

    SQLITE_FILE = ROOT_DIR / "database.sqlite3"
    """ /database.sqlite3 """
