#
# Export enchant data
#

from __future__ import annotations

from typing import ClassVar, Dict
import attr
import functools

from ._base import horsaga_db

@attr.s(slots=True, auto_attribs=True)
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

    @lookup.register(int)
    @classmethod
    def _(cls, lookup_arg: int): # search by ID
        return cls._cache.get(lookup_arg)

    @lookup.register(str)
    @classmethod
    def _(cls, lookup_arg: str): # search by name
        result = []
        for row in horsaga_db.execute(
            'SELECT id FROM enchant WHERE name = ?', (lookup_arg,)):
            result.append(cls._cache.get(row[0]))
        return result

    # TODO search by special skill or support skill name / ID

Enchant.__module__ = __spec__.parent


def _populate():
    for row in horsaga_db.execute('SELECT id, name FROM enchant'):
        _ = Enchant(**row)

_populate()