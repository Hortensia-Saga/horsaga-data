#
# Type stub for horsaga-data
#

from typing import (
    List,
    Optional,
    Pattern,
    Tuple,
    TypeVar,
    overload,
)
import sqlite3
import enum
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

class AtkAttr(EnumRegexMixin, enum.Enum):
    @property
    def value(self) -> int: ...
    @property
    def code(self) -> str: ...
    @property
    def kanji(self) -> str: ...
    @property
    def color(self) -> str: ...
    @property
    def combined(self) -> str: ...

class Rarity(enum.Enum):
    @property
    def value(self) -> int: ...
    @property
    def code(self) -> str: ...
    @property
    def full_name(self) -> str: ...

class SpeedRank(enum.Enum):
    @property
    def value(self) -> int: ...
    @property
    def code(self) -> str: ...

@attr.s
class Enchant:
    id: int
    name: str
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: str) -> List[_T]: ...

@attr.s
class Skill:
    id: int
    code: str
    name: str
    desc: str
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: str) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: Pattern) -> List[_T]: ...

@attr.s
class Tactic:
    id: int
    code: str
    name: str
    desc: str
    tp_cost: int
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: int) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: str) -> Optional[_T]: ...
    @overload
    @classmethod
    def lookup(cls: _T, lookup_arg: Pattern) -> List[_T]: ...

@attr.s
class Character:
    id: int
    name: str
    attr: AtkAttr
    @classmethod
    def lookup(cls: _T, lookup_arg: int) -> Optional[_T]: ...

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
    flag: int
    skill: Skill
    uf: Skill
    tactic: Tuple[Tactic, ...]
    enchant: Enchant
    kn_skill: Skill
    @classmethod
    def lookup(cls: _T, lookup_arg: int) -> Optional[_T]: ...