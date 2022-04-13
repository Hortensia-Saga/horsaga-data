============
horsaga.data
============

.. raw:: html

    <img src="https://github.com/Hortensia-Saga/horsaga-data/actions/workflows/build.yml/badge.svg" alt="Testing workflow badge" />

Exports Hortensia Saga card data and other constants as python structure.

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

DB building
***********

Scripts used for mining card data are placed inside ``data_mining`` folder.
They are only placed here for reference, as the scripts require proper setup
of Hortensia Saga accounts and config, as well as the ``horsaga`` package.
