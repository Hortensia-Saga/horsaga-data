#
# Generate stub for enum members
#

import csv
from io import StringIO
from textwrap import dedent
from typing import Iterable, NamedTuple, Optional, Tuple, Union

from _common import RAW_DATA_DIR, SRC_DIR

FILENAME = SRC_DIR / '_enum_members.pyi'


class _EnumDefs(NamedTuple):
    filename: str
    cls_name: str
    use_regex_mixin: bool
    props: Union[Tuple[str, ...], bool]  # True=all fields, False=no
    member_name: Optional[str]  # None = no member listing


tbls = [
    _EnumDefs(
        'attack_attrib.csv',
        'AtkAttr',
        True,
        True,
        'code',
    ),
    _EnumDefs(
        'rarity.csv',
        'Rarity',
        False,
        True,
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
        True,
        None,
    ),
    _EnumDefs(
        'ability_mat_type.csv',
        'AbilityMatType',
        True,
        True,
        'type',
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
        assert reader.fieldnames is not None
        # write members
        if data.member_name:
            for row in reader:
                output.write(f'{indent}{row[data.member_name]} = ...\n')

        # write fake properties
        fieldnames: Iterable[str] = (
            data.props
            if isinstance(data.props, tuple)
            else reader.fieldnames
            if data.props is True
            else ()
        )
        for field in fieldnames:
            if (  # FIXME reuse definitions in build_db.py
                field == 'value'
                or field.startswith('min_')
                or field.startswith('max_')
                or "id" in field
            ):
                type_ = 'int'
            else:
                type_ = 'str'
            output.write(
                f'{indent}@property\n{indent}def {field}(self) -> {type_}: ...\n'
            )

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
