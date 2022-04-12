#
# Pre-generate all formation sheets as attrs instance
#

from __future__ import annotations

import functools
from types import MappingProxyType
from typing import ClassVar, Dict

import attr

from ._base import horsaga_db


# TODO bonus attribute on each square,
# but need to complete attribute flags first
@attr.s(slots=True, frozen=True, auto_attribs=True)
class Formation:
    _cache: ClassVar[Dict[int, Formation]] = {}
    id: int
    name: str
    desc: str
    type: int

    def __attrs_post_init__(self):
        type(self)._cache[self.id] = self

    @classmethod
    def cache(cls) -> MappingProxyType[int, Formation]:
        return MappingProxyType(cls._cache)

    @functools.singledispatchmethod
    @classmethod
    def lookup(cls, lookup_arg):
        raise TypeError(f'Lookup argument type {type(lookup_arg)} not supported')

    @lookup.register(int)
    @classmethod
    def _(cls, lookup_arg: int):  # search by ID
        return cls._cache.get(lookup_arg)

    @lookup.register(str)
    @classmethod
    def _(cls, lookup_arg: str):  # search by name
        resultset = [
            row[0]
            for row in horsaga_db.execute(
                'SELECT id FROM formation WHERE name = ?', (lookup_arg,)
            )
        ]
        # formation sheet names guaranteed unique in DB
        if len(resultset):
            return cls._cache.get(resultset[0])

    # TODO search sheet by formation type


Formation.__module__ = __spec__.parent

for row in horsaga_db.execute('SELECT * FROM formation'):
    _ = Formation(**row)  # Accessible via Formation.lookup()
