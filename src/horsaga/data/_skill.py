#
# Pre-generate all skills as attrs instance
#

from __future__ import annotations

import functools
import re
from typing import ClassVar, Dict

import attr

from ._base import horsaga_db


@attr.s(frozen=True, auto_attribs=True)
class Skill:
    _cache: ClassVar[Dict[int, Skill]] = {}
    id: int
    code: str
    name: str
    desc: str
    # TODO Skill effect as attributes and/or flags
    # TODO Maybe create flag for knight skill and UF skill

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
            'SELECT id FROM skill WHERE name = ?', (lookup_arg,))]
        # skill name guaranteed unique in DB schema
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

Skill.__module__ = __spec__.parent


def _populate():
    # TODO Think about replacing sqlite3 row_factory temporarily
    for row in horsaga_db.execute('SELECT * FROM skill'):
        _ = Skill(**row) # Accessible via Skill.lookup()

_populate()
