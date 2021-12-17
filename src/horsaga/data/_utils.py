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

        return '|'.join(re.escape(getattr(e, attr)) for e in list(cls))

    @classmethod
    def char_class_re(cls, attr: str = 'value') -> str:
        """Create character class regex like ``[awx]`` from enum members

        Raises
        ------
        ValueError
            When attribute of any member has string length > 1
        """

        for e in list(cls):
            if len(getattr(e, attr)) <= 1:
                continue
            raise ValueError(f'Attribute "{attr}" '
                f'of member {e!r} contains multiple char')

        return (
            '[' +
            "".join(re.escape(getattr(e, attr)) for e in list(cls)) +
            ']'
        )


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
