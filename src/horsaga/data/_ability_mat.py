#
# Ability orb material types
#

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from ._base import horsaga_db
from ._utils import EnumRegexMixin

_table = 'ability_mat_type'


class AbilityMatType(EnumRegexMixin, enum.Enum):
    """Basic orbs for composing an ability orb"""

    _ignore_ = ['AbilityMatType', 'row']
    AbilityMatType = vars()
    for row in horsaga_db.execute(f'SELECT * FROM {_table}'):
        AbilityMatType[row['type']] = row['gid']

    if TYPE_CHECKING:

        def __setitem__(self, __k, __v):
            ...  # for pyright

    # attribute aliases
    @property
    def gid(self) -> int:
        return self.value

    @property
    def type(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<{type(self).__qualname__}.{self.name}>'


AbilityMatType.__module__ = __spec__.parent
