============
horsaga.data
============

.. raw:: html

    <img src="https://github.com/Hortensia-Saga/horsaga-data/actions/workflows/testing.yml/badge.svg" alt="Testing workflow badge" />

Exports Hortensia Saga card data and other constants as python structure.

Dependencies
************

- All data stored in `SQLite`_ database.
- Uses `Attrs`_ for class structure.
- Utilize `PDM`_ as PEP 517 build backend.
- `Tox`_ for test automation.

Usage
*****

``import horsaga.data``

Simple as that. In particular, a Sqlite3 connection object
``horsaga_db`` is exported so that one can do custom read-only access
to database. Read-write access is not planned for now.

.. _SQLite: https://www.sqlite.org/
.. _Attrs: https://www.attrs.org/
.. _PDM: https://pdm.fming.dev/
.. _Tox: https://tox.wiki/