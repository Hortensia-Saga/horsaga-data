#
# Character data which can be shared across multiple cards
#

from __future__ import annotations

import functools
from typing import ClassVar, Dict

import attr

from ._attrib import AtkAttr
from ._base import horsaga_db


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Character:
    """Character data shared (potentially) across multiple cards"""
    _cache: ClassVar[Dict[int, Character]] = {}
    id: int
    name: str
    attr: AtkAttr = attr.field(converter=AtkAttr)
    # TODO data for awaken stat gain ratio

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

Character.__module__ = __spec__.parent


for row in horsaga_db.execute('SELECT id, name, attr FROM chara'):
    _ = Character(**row) # Accessible via Character.lookup()
