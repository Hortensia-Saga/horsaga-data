#
# Pre-generate all tactics as attrs instance
#

from __future__ import annotations

from typing import ClassVar, Dict
import attr
import functools
import re

from ._base import horsaga_db

# FIXME ID may not be unique if Old Amulet Tactics are included
# A bunch of tactics would be available in alternative form in
# Old Amulet event, e.g. FooBar Tactics -> FooBar Gem Tactics,
# yet tactic ID is retained. This makes tactic name the only
# unique key for identification.
@attr.s(frozen=True, auto_attribs=True)
class Tactic:
    _cache: ClassVar[Dict[int, Tactic]] = {}
    id: int
    code: str
    name: str
    desc: str
    tp_cost: int

    def __attrs_post_init__(self):
        type(self)._cache[self.id] = self

    @functools.singledispatchmethod
    @classmethod
    def lookup(cls, lookup_arg):
        raise TypeError(f'Lookup argument type {type(lookup_arg)} not supported')

    # BUG @register failed to read annotation from function signature
    @lookup.register(int)
    @classmethod
    def _(cls, lookup_arg: int): # search by ID
        return cls._cache.get(lookup_arg)

    @lookup.register(str)
    @classmethod
    def _(cls, lookup_arg: str): # search by name
        resultset = [row[0] for row in horsaga_db.execute(
            'SELECT id FROM tactic WHERE name = ?', (lookup_arg,))]
        # tactic name guaranteed unique in DB schema
        if len(resultset):
            return cls._cache.get(resultset[0])

    @lookup.register(re.Pattern)
    @classmethod
    def _(cls, lookup_arg: re.Pattern): # search by name/desc regex
        # Python sqlite3 module does not support loadable extension,
        # so sqlite3 regexp is unusable. We do search without SQL.
        result = []
        for skill_obj in cls._cache.values():
            if (lookup_arg.search(skill_obj.name) or
                lookup_arg.search(skill_obj.desc)):
                result.append(skill_obj)
        return result

Tactic.__module__ = __spec__.parent


def _populate():
    for row in horsaga_db.execute('SELECT * FROM tactic'):
        _ = Tactic(**row) # Accessible via Tactic.lookup()

_populate()