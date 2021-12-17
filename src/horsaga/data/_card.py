#
# Basic, non-volatile Hortensia Saga card data
#

from __future__ import annotations

from typing import ClassVar, Dict, Tuple
import attr
import functools

from ._base import horsaga_db
from ._speed import SpeedRank
from ._rarity import Rarity
from ._character import Character
from ._skill import Skill
from ._tactic import Tactic
from ._enchant import Enchant

@attr.s(slots=True, auto_attribs=True)
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
    flag: int # TODO convert to useful enum flags
    skill: Skill = attr.field(
        converter=lambda x: None if x is None else Skill.lookup(x))
    uf: Skill = attr.field(
        converter=lambda x: None if x is None else Skill.lookup(x))
    tactic: Tuple[Tactic, ...]
    enchant: Enchant = attr.field(
        converter=lambda x: None if x is None else Enchant.lookup(x))
    kn_skill: Skill = attr.field(
        converter=lambda x: None if x is None else Skill.lookup(x))

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

CardBase.__module__ = __spec__.parent


def _populate():
    for row in horsaga_db.execute('SELECT * FROM cardbase'):
        kwds = dict(row)
        tactic_list = []
        for key in ('tactic1', 'tactic2'):
            if (tid := kwds.pop(key)):
                tactic_list.append(Tactic.lookup(tid))
        kwds['tactic'] = tuple(tactic_list)
        _ = CardBase(**kwds)

_populate()

# TODO dummy card class for internal-only fake cards
# some attribs (speed, chara, tactic etc) are totally useless