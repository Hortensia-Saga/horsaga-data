#
# Export enchant data
#

from __future__ import annotations

import functools
from typing import ClassVar, Dict

import attr

from ._base import horsaga_db


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Enchant:
    """Enchant data"""
    _cache: ClassVar[Dict[int, Enchant]] = {}
    id: int
    name: str
    # TODO Most data not available yet, waiting for DB

    def __attrs_post_init__(self):
        type(self)._cache[self.id] = self

    @functools.singledispatchmethod
    @classmethod
    def lookup(cls, lookup_arg):
        raise TypeError(f'Lookup argument type {type(lookup_arg)} not supported')

    @lookup.register(int) # by ID
    @classmethod
    def _(cls, lookup_arg: int):
        return cls._cache.get(lookup_arg)

    @lookup.register(str) # by name
    @classmethod
    def _(cls, lookup_arg: str):
        resultset = [row[0] for row in horsaga_db.execute(
            'SELECT id FROM enchant WHERE name = ?', (lookup_arg,))]
        return frozenset(cls._cache.get(id) for id in resultset)

    # TODO search by special skill or support skill name / ID

Enchant.__module__ = __spec__.parent

for row in horsaga_db.execute('SELECT id, name FROM enchant'):
    _ = Enchant(**row)
