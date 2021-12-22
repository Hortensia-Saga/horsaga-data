#
# Export Attack attribute constants
#

import enum
from collections import namedtuple
from typing import TYPE_CHECKING

from ._base import horsaga_db
from ._utils import EnumMultiValueMixin

_table = 'speed'
_field_names = [row[0]
    for row in horsaga_db.execute(
        f'SELECT name FROM PRAGMA_TABLE_INFO("{_table}")')]
_fields = namedtuple('_SpeedRank_Fields', _field_names)

class SpeedRank(EnumMultiValueMixin, _fields, enum.Enum):
    """Code and value representing unit speed"""
    _ignore_ = ['SpeedRank', 'row', '_rank_tr']

    # Symbols not acceptable as enum member name
    # e.g. SS+ -> SSP, A- -> AM
    _rank_tr = str.maketrans('+-', 'PM')

    SpeedRank = vars()
    for row in horsaga_db.execute(f'SELECT value, code FROM {_table}'):
        SpeedRank[row['code'].translate(_rank_tr)] = tuple(row)

    if TYPE_CHECKING:
        @property
        def code(self) -> str: ...
        @property
        def value(self) -> str: ...

    def __repr__(self) -> str:
        return f'<{type(self).__qualname__}:{self.code} ({self.value})>'

SpeedRank.__module__ = __spec__.parent