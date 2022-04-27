#
# Create read-only connection to sqlite database
#

import sqlite3
from pathlib import Path
from urllib.parse import urlunsplit

__all__ = ['horsaga_db']

# Create a memory copy of DB
# If db file is kept open, package upgrade would cause trouble on Windows
def prepare_mem_db(file: Path) -> sqlite3.Connection:
    file_uri = urlunsplit(('file', '', str(file), '', 'mode=ro'))
    src = sqlite3.connect(file_uri, uri=True)
    dest = sqlite3.connect(':memory:')
    src.backup(dest)
    src.close()
    dest.execute('PRAGMA query_only = 1;')
    return dest

db_file = Path(__file__).parent / 'horsaga.sqlite3'
horsaga_db = prepare_mem_db(db_file)
horsaga_db.row_factory = sqlite3.Row
