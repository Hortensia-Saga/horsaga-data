#
# Utility classes and functions
#

import enum
import re

class EnumRegexMixin(enum.Enum):
    """Mixin class allowing a enum class to compose alternation
    regex and character class regex using attributes from its members.
    """

    @classmethod
    def alternation_re(cls, attr: str = 'value') -> str:
        """Create alternation regex ``foo|bar`` from enum members"""

        values = [getattr(e, attr) for e in list(cls)]
        return '|'.join(re.escape(v) for v in values if isinstance(v, str) and len(v))

    @classmethod
    def char_class_re(cls, attr: str = 'value') -> str:
        """Create character class regex like ``[awx]`` from enum members

        Raises
        ------
        ValueError
            When attribute of any member has string length > 1
        """

        values = []
        for e in list(cls):
            if not (v := getattr(e, attr)) or not isinstance(v, str):
                continue
            if len(v) != 1:
                raise ValueError(f'Attribute "{attr}" '
                    f'of member {e!r} contains multiple char')
            values.append(v)

        return ('[{}]'.format("".join(re.escape(v) for v in values)))


# The downside for this approach is, type checkers may expect enum value
# reverse lookup to take the full mix-in type fields as argument. For example:
#     class MyType(NamedTuple):
#         desc: str
#         alias: str
#     class MyEnum(EnumMutiValueMixin, MyType, Enum):
#         ITEM1: 'FooBar', 'stock1'
# We want MyEnum('FooBar') == MyEnum('stock1') == MyEnum.ITEM1,
# but pyright currently expects signature MyEnum(('FooBar', 'stock1'))
# Therefore in the end something still needs to be type ignored.
class EnumMultiValueMixin(enum.Enum):
    """Mixin for emulating aenum.MultiValueEnum without aenum module"""
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            type(self)._value2member_map_[arg] = self
