from pathlib import Path


class Paths:
    ROOT_DIR = Path(__file__).parent.parent.parent
    """ / """

    ENV_FILE = ROOT_DIR / ".env"
    """ /.env """

    SQLITE_FILE = ROOT_DIR / "database.sqlite3"
    """ /database.sqlite3 """

    MIGRATIONS_DIR = ROOT_DIR / "migrations"
    """ /migrations/ """

    FIXTURES_DIR = ROOT_DIR / "fixtures"
    """ /fixtures/ """

    ADMIN_USER_JSON_FILE = FIXTURES_DIR / "01_admin_user.json"
    """ /fixtures/01_admin_user.json """

    DEFAULT_PAYMENT_METHODS_JSON_FILE = FIXTURES_DIR / "02_default_payment_methods.json"
    """ /fixtures/02_default_payment_methods.json """
