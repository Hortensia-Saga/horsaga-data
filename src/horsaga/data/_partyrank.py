#
# Export Attack attribute constants
#

import enum
from collections import namedtuple
from typing import TYPE_CHECKING

from ._base import horsaga_db
from ._utils import EnumMultiValueMixin

_table = 'rank'
_field_names = [row[0]
    for row in horsaga_db.execute(
        f'SELECT name FROM PRAGMA_TABLE_INFO("{_table}")')]
_fields = namedtuple('_PartyRank_Fields', _field_names)

class PartyRank(EnumMultiValueMixin, _fields, enum.Enum):
    """Ranking for GVG or Quest party"""
    _ignore_ = ['PartyRank', 'row', '_rank_tr']

    # Symbols not acceptable as enum member name
    # e.g. SS+ -> SSP, A- -> AM
    _rank_tr = str.maketrans('+-', 'PM')

    PartyRank = vars()
    for row in horsaga_db.execute(f'SELECT * FROM {_table}'):
        PartyRank[row['code'].translate(_rank_tr)] = tuple(row)

    def __init__(self, *args):
        super().__init__()
        for arg in args[:2]: # reverse lookup on numeric value and code only
            type(self)._value2member_map_[arg] = self

    if TYPE_CHECKING:
        @property
        def code(self) -> str: ...

    def __repr__(self) -> str:
        return f'<{type(self).__qualname__}:{self.code}>'

PartyRank.__module__ = __spec__.parent