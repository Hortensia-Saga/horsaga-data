#
# Basic, non-volatile Hortensia Saga card data
#

from __future__ import annotations

import enum
import functools
from types import MappingProxyType
from typing import ClassVar, Dict, Tuple

import attr

from ._base import horsaga_db
from ._character import Character
from ._enchant import Enchant
from ._rarity import Rarity
from ._skill import Skill
from ._speed import SpeedRank
from ._tactic import Tactic


class CardBaseFlag(enum.Flag):
    NONE = 0
    HERO = 1
    DUMMY = 2

    def __repr__(self) -> str:
        return f'<{type(self).__name__}.{self._name_}>'

CardBaseFlag.__module__ = __spec__.parent

@attr.s(slots=True, frozen=True, auto_attribs=True)
class CardBase:
    _cache: ClassVar[Dict[int, CardBase]] = {}
    id: int
    title: str
    hp: int
    attack: int
    defend: int
    speed: SpeedRank = attr.field(converter=SpeedRank)
    bp: int
    rare: Rarity = attr.field(converter=Rarity)
    chara: Character = attr.field(
        converter=lambda x: None if x is None else Character.lookup(x))
    flag: CardBaseFlag = attr.field(converter=CardBaseFlag)
    skill: Skill = attr.field(
        converter=lambda x: None if x is None else Skill.lookup(x))
    uf: Skill = attr.field(
        converter=lambda x: None if x is None else Skill.lookup(x))
    tactic: Tuple[Tactic, ...]
    enchant: Enchant = attr.field(
        converter=lambda x: None if x is None else Enchant.lookup(x))
    kn_skill: Skill = attr.field(
        converter=lambda x: None if x is None else Skill.lookup(x))

    def __str__(self) -> str:
        return (f'<{type(self).__name__} {self.id} ({self.title})>')

    def __attrs_post_init__(self):
        type(self)._cache[self.id] = self

    @classmethod
    def cache(cls) -> MappingProxyType[int, CardBase]:
        return MappingProxyType(cls._cache)

    @functools.singledispatchmethod
    @classmethod
    def lookup(cls, lookup_arg):
        raise TypeError(f'Lookup argument type {type(lookup_arg)} not supported')

    # BUG @register failed to read annotation from function signature
    @lookup.register(int)
    @classmethod
    def _(cls, lookup_arg: int): # search by ID
        return cls._cache.get(lookup_arg)

CardBase.__module__ = __spec__.parent


for row in horsaga_db.execute('SELECT * FROM cardbase'):
    kwds = dict(row)
    tactic_list = []
    for key in ('tactic1', 'tactic2'):
        if (tid := kwds.pop(key)):
            tactic_list.append(Tactic.lookup(tid))
    kwds['tactic'] = tuple(tactic_list)
    _ = CardBase(**kwds)

# TODO dummy card class for internal-only fake cards
# some attribs (speed, chara, tactic etc) are totally useless
