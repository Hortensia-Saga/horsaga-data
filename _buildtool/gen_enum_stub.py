#
# Generate stub for enum members
#

import csv
from io import StringIO
from textwrap import dedent
from typing import NamedTuple, Optional, Tuple

from _common import RAW_DATA_DIR, SRC_DIR

FILENAME = SRC_DIR / '_enum_members.pyi'


class _EnumDefs(NamedTuple):
    filename: str
    cls_name: str
    use_regex_mixin: bool
    props: Optional[Tuple[str, ...]]  # None = all fields are used
    member_name: Optional[str]  # None = no member listing


tbls = [
    _EnumDefs(
        'attack_attrib.csv',
        'AtkAttr',
        True,
        None,
        'code',
    ),
    _EnumDefs(
        'rarity.csv',
        'Rarity',
        False,
        None,
        'code',
    ),
    _EnumDefs(
        'rank.csv',
        'SpeedRank',
        False,
        ('value', 'code'),
        None,
    ),
    _EnumDefs(
        'rank.csv',
        'PartyRank',
        False,
        None,
        None,
    ),
]


def get_header() -> str:
    header = """\
    ###################################################
    #
    # This enum stub file is automatically generated.
    # Any modifications will not be preserved.
    #
    ###################################################

    import enum
    from . import EnumRegexMixin
    """
    return dedent(header)


def get_enum_stub(data: _EnumDefs) -> str:
    # StringIO + context manager proposal is rejected (bpo-43834)
    output = StringIO()
    indent = '    '

    # TODO ast.unparse for python 3.9
    inherited = ['enum.Enum']
    if data.use_regex_mixin:
        inherited.insert(0, 'EnumRegexMixin')
    output.write('\nclass {}({}):\n'.format(data.cls_name, ', '.join(inherited)))

    with open(
        RAW_DATA_DIR / data.filename, mode='r', newline='', encoding='utf-8'
    ) as f:
        reader = csv.DictReader(f)
        # write members
        if data.member_name:
            for row in reader:
                output.write(f'{indent}{row[data.member_name]} = ...\n')

        # write fake properties
        fieldnames = data.props if data.props else reader.fieldnames
        for field in fieldnames:
            # fmt: off
            if ( # OK this is cheating
                field == 'value' or
                field.startswith('min_') or
                field.startswith('max_')
            ): # fmt: on
                type_ = 'int'
            else:
                type_ = 'str'
            # fmt: off
            output.write(
                f'{indent}@property\n'
                f'{indent}def {field}(self) -> {type_}: ...\n'
            )
            # fmt: on

    content = output.getvalue()
    output.close()
    return content


#
# The real thing
#
with open(FILENAME, mode='w', newline=None) as f:
    f.write(get_header())
    for tbl in tbls:
        f.write(get_enum_stub(tbl))
