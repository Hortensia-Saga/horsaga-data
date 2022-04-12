#
# Type stub for horsaga-data
#

import enum
import sqlite3
from types import MappingProxyType
from typing import Optional, Pattern, Type, TypeVar, overload

import attr

_T = TypeVar('_T')

horsaga_db: sqlite3.Connection

class EnumRegexMixin:
    @classmethod
    def alternation_re(cls, attr: str = ...) -> str: ...
    @classmethod
    def char_class_re(cls, attr: str = ...) -> str: ...

# Add superfluous properties to each enum instead
# However, all enums won't have data type fixated,
# otherwise type checker would complain about wrong type
# in reverse enum lookup argument.
class EnumMultiValueMixin:
    pass

@attr.s
class Enchant:
    id: int
    name: str
    @classmethod
    def cache(cls) -> MappingProxyType[int, Enchant]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: str) -> frozenset[_T]: ...

@attr.s
class Formation:
    id: int
    name: str
    desc: str
    type: int
    @classmethod
    def cache(cls) -> MappingProxyType[int, Formation]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: str) -> Optional[_T]: ...

@attr.s
class Skill:
    id: int
    code: str
    name: str
    desc: str
    @classmethod
    def cache(cls) -> MappingProxyType[int, Skill]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: str) -> frozenset[_T]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: Pattern) -> frozenset[_T]: ...

@attr.s
class Tactic:
    id: int
    code: str
    name: str
    desc: str
    tp_cost: int
    @classmethod
    def cache(cls) -> MappingProxyType[int, Tactic]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: str) -> frozenset[_T]: ...
    @overload
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: Pattern) -> frozenset[_T]: ...

@attr.s
class Character:
    id: int
    name: str
    attr: AtkAttr
    @classmethod
    def cache(cls) -> MappingProxyType[int, Character]: ...
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: int) -> Optional[_T]: ...

class CardBaseFlag(enum.Flag):
    NONE = ...
    HERO = ...
    DUMMY = ...

@attr.s
class CardBase:
    id: int
    title: str
    hp: int
    attack: int
    defend: int
    speed: SpeedRank
    bp: int
    rare: Rarity
    chara: Character
    flag: CardBaseFlag
    skill: Skill
    uf: Skill
    tactic: tuple[Tactic, ...]
    enchant: Enchant
    kn_skill: Skill
    @classmethod
    def cache(cls) -> MappingProxyType[int, CardBase]: ...
    @classmethod
    def lookup(cls: Type[_T], lookup_arg: int) -> Optional[_T]: ...

# isort: off
from ._enum_members import (
    AtkAttr   as AtkAttr,
    Rarity    as Rarity,
    PartyRank as PartyRank,
    SpeedRank as SpeedRank,
)

# isort: on
