#
# Utility classes and functions
#

import enum
import re
from collections import defaultdict
from typing import Iterable


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


class EnumMultiValueMixin(enum.Enum):
    """Mixin for emulating :class:`aenum.MultiValueEnum` without aenum module

    When using this mixin class, the mixin type of enum must be namedtuple
    (each tuple item can be accessed as attribute from enum member).

    Notes
    -----
    Two mutually exclusive keyword arguments are available during
    enum construction:

    lookup_enable: Iterable[str], optional
        List of attribute names to whitelist when constructing reverse lookup
        dict. Only those values under specified attributes are searchable.

    lookup_disable: Iterable[str], optional
        List of attribute names to ignore when constructing reverse lookup dict.
        Lookup of values from these attributes would result in exception.

    Once these arguments are used, Python 3.9.2+ becomes a hard requirement;
    otherwise python version restriction does not apply.
    """
    def __init_subclass__(
        cls, /,
        lookup_enable: Iterable[str] = None,
        lookup_disable: Iterable[str] = None,
        **kwds
    ) -> None:
        super().__init_subclass__(**kwds)
        lookup_enable = set(lookup_enable) if lookup_enable else set()
        lookup_disable = set(lookup_disable) if lookup_disable else set()
        if len(lookup_enable):
            if len(lookup_disable):
                raise ValueError('lookup_enable and lookup_disable '
                    'must not be used together')
            lookup_dict = defaultdict(lambda: False)
            for fname in lookup_enable:
                lookup_dict[fname] = True
        else:
            lookup_dict = defaultdict(lambda: True)
            for fname in lookup_disable:
                lookup_dict[fname] = False
        cls._field_in_lookup = lookup_dict


    def __init__(self, *args):
        super().__init__()
        if getattr(type(self), '_field_in_lookup', None) is None:
            # Py < 3.9.2, where __init_subclass__ is not called
            for arg in args:
                type(self)._value2member_map_[arg] = self
            return
        me = self._value_._asdict()
        in_lookup = type(self)._field_in_lookup
        accepted_vals = [v for k, v in me.items()
            if in_lookup[k]]
        for v in accepted_vals:
            type(self)._value2member_map_[v] = self
