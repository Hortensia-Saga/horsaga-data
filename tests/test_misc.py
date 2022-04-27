#
# Test: Miscellaneous stuff
#

import sqlite3

import pytest


@pytest.mark.xfail(reason='should be read-only', raises=sqlite3.OperationalError)
def test_db_write():
    from horsaga.data import horsaga_db

    cursor = horsaga_db.execute('INSERT INTO rank (value, code) VALUES(0, "SS14");')
