#
# Export Attack attribute constants
#

import enum
from collections import namedtuple
from typing import TYPE_CHECKING

from ._base import horsaga_db
from ._utils import EnumMultiValueMixin

# Out of 3 fields (value, code, full_name),
# 'code' is taken as the enum name
_table = 'rarity'
_name_pos = 1

_field_names = [row[0]
    for row in horsaga_db.execute(
        f'SELECT name FROM PRAGMA_TABLE_INFO("{_table}")')]
_field_names.pop(_name_pos)
_fields = namedtuple('_Rarity_Fields', _field_names)

class Rarity(EnumMultiValueMixin, _fields, enum.Enum):
    """Card rarity (N, R, SR etc) commonly seen in mobile games"""

    _ignore_ = ['Rarity', 'row']

    Rarity = vars()
    for row in horsaga_db.execute(f'SELECT * FROM {_table}'):
        Rarity[row[_name_pos]] = row[0:_name_pos] + row[(_name_pos+1):]

    if TYPE_CHECKING:
        @property
        def value(self) -> int: ...

    def __repr__(self) -> str:
        return f'<{type(self).__qualname__}.{self.name}: {self.value}>'

Rarity.__module__ = __spec__.parent