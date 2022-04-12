#
# Test: EnumMultiValueMixin with whitelisted / ignored fields
# Excluded for python < 3.9
#

import enum
from collections import namedtuple

import pytest

from horsaga.data import EnumMultiValueMixin

_fields = namedtuple('_MyFields', ('attr1', 'attr2', 'attr3', 'attr4'))


class ModFour(
    EnumMultiValueMixin, _fields, enum.Enum, lookup_enable=('attr1', 'attr3')
):
    # fmt: off
    ZERO  = (0, 4,  8, 'doh')
    ONE   = (1, 5,  9, 'doh')
    TWO   = (2, 6, 10, 'doh')
    THREE = (3, 7, 11, 'doh')
    # fmt: on


def test_multivalue_include():
    assert ModFour(1) == ModFour.ONE
    assert ModFour(9) == ModFour.ONE
    with pytest.raises(ValueError):
        ModFour(5)
    with pytest.raises(ValueError):
        ModFour('doh')


class ModFourAlt(
    EnumMultiValueMixin, _fields, enum.Enum, lookup_disable=('attr3', 'junk')
):
    # fmt: off
    ZERO  = (0, 4,  8, 'doh')
    ONE   = (1, 5,  9, 'doh')
    TWO   = (2, 6, 10, 'doh')
    THREE = (3, 7, 11, 'doh')
    # fmt: on


def test_multivalue_exclude():
    assert ModFourAlt(1) == ModFourAlt.ONE
    assert ModFourAlt(5) == ModFourAlt.ONE
    with pytest.raises(ValueError):
        ModFourAlt(9)
    # Last enum member wins, but we don't depend on such behavior
    # Generally such fields should be excluded instead
    assert isinstance(ModFourAlt('doh'), ModFourAlt)
