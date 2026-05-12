from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent.parent
''' / '''

ENV_FILE = ROOT_DIR / '.env'
''' /.env '''

SQLITE_FILE = ROOT_DIR / 'database.sqlite3'
''' /database.sqlite3 '''
