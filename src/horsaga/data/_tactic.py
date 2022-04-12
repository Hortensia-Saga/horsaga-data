#
# Pre-generate all tactics as attrs instance
#

from __future__ import annotations

import functools
import re
from types import MappingProxyType
from typing import ClassVar, Dict

import attr

from ._base import horsaga_db


# FIXME ID may not be unique if Old Amulet Tactics are included
# A bunch of tactics would be available in alternative form in
# Old Amulet event, e.g. FooBar Tactics -> FooBar Gem Tactics,
# yet tactic ID is retained. This makes tactic name the only
# unique key for identification.
@attr.s(slots=True, frozen=True, auto_attribs=True)
class Tactic:
    _cache: ClassVar[Dict[int, Tactic]] = {}
    id: int
    code: str
    name: str
    desc: str
    tp_cost: int

    def __attrs_post_init__(self):
        type(self)._cache[self.id] = self

    @classmethod
    def cache(cls) -> MappingProxyType[int, Tactic]:
        return MappingProxyType(cls._cache)

    @functools.singledispatchmethod
    @classmethod
    def lookup(cls, lookup_arg):
        raise TypeError(f'Lookup argument type {type(lookup_arg)} not supported')

    # BUG @register failed to read annotation from function signature
    @lookup.register(int) # by ID
    @classmethod
    def _(cls, lookup_arg: int):
        return cls._cache.get(lookup_arg)

    @lookup.register(str) # by name/code
    @classmethod
    def _(cls, lookup_arg: str):
        resultset = [row[0] for row in horsaga_db.execute(
            'SELECT id FROM tactic WHERE name = ? OR code = ?',
            (lookup_arg, lookup_arg))]
        # though name is unique, code isn't
        return frozenset(cls._cache.get(id) for id in resultset)

    @lookup.register(re.Pattern) # by name/desc/code regex
    @classmethod
    def _(cls, lookup_arg: re.Pattern):
        # Python sqlite3 module does not support loadable extension
        # by default. Thus search without SQL -- a bit expensive though.
        return frozenset(
            obj for obj in cls._cache.values()
            if (lookup_arg.search(obj.name) or
                lookup_arg.search(obj.code) or
                lookup_arg.search(obj.desc)))

Tactic.__module__ = __spec__.parent

for row in horsaga_db.execute('SELECT * FROM tactic'):
    _ = Tactic(**row) # Accessible via Tactic.lookup()
