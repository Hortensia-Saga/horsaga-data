#
# Create read-only connection to sqlite database
#

import sqlite3
from pathlib import Path
from urllib.parse import urlunsplit

__all__ = ['horsaga_db']

db_file = Path(__file__).parent / 'horsaga.sqlite3'
db_uri = urlunsplit(('file', '', str(db_file), '', 'mode=ro'))

horsaga_db = sqlite3.connect(db_uri, uri=True)
horsaga_db.row_factory = sqlite3.Row
