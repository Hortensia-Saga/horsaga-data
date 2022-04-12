#
# Export Attack attribute constants
#

import enum
from collections import namedtuple
from typing import TYPE_CHECKING

from ._base import horsaga_db
from ._utils import EnumMultiValueMixin, EnumRegexMixin

_table = 'attack_attrib'
_field_names = [row[0]
    for row in horsaga_db.execute(
        f'SELECT name FROM PRAGMA_TABLE_INFO("{_table}")')]
_fields = namedtuple('_AtkAttr_Fields', _field_names)

class AtkAttr(EnumMultiValueMixin, EnumRegexMixin, _fields, enum.Enum):
    """The 4 basic unit attributes (斬, 突, 打, 遠)"""

    _ignore_ = ['AtkAttr', 'row']

    AtkAttr = vars()
    # Out of 5 fields (value, code, kanji, color, combined),
    # 'code' is taken as the enum name
    for row in horsaga_db.execute(f'SELECT * FROM {_table}'):
        AtkAttr[row['code']] = tuple(row)

    if TYPE_CHECKING:
        @property
        def kanji(self) -> str: ...
        def __setitem__(self, __k, __v): ...  # for pyright

    def __repr__(self) -> str:
        return f'<{type(self).__qualname__}.{self.name}: {self.kanji}>'

AtkAttr.__module__ = __spec__.parent
