#
# Test: EnumMultiValueMixin works for enums
#

import enum
import sys
from collections import namedtuple
from random import choice

import pytest

from horsaga.data import EnumMultiValueMixin


def test_attr_roundtrip():
    from horsaga.data import AtkAttr
    e = choice(list(AtkAttr))
    for v in e._value_:
        assert AtkAttr(v) == e

def test_rarity_roundtrip():
    from horsaga.data import Rarity
    e = choice(list(Rarity))
    for v in e._value_:
        assert Rarity(v) == e

def test_speed_roundtrip():
    from horsaga.data import SpeedRank
    e = choice(list(SpeedRank))
    for v in e._value_:
        assert SpeedRank(v) == e

def test_partyrank_roundtrip():
    from horsaga.data import PartyRank
    e = choice(list(PartyRank))
    for v in e._value_[:2]:
        assert PartyRank(v) == e

#
# Test: EnumRegexMixin works for AtkAttr
#

@pytest.mark.parametrize("field, expected", [
    pytest.param('kanji', r'[斬突打遠]', id='chr-kanji'),
    pytest.param('color', r'[紅蒼紫翠]', id='chr-color')
])
def test_attr_chr_re(field, expected):
    from horsaga.data import AtkAttr
    assert AtkAttr.char_class_re(field) == expected

@pytest.mark.parametrize("field, expected", [
    pytest.param('kanji', r'斬|突|打|遠', id='alt-kanji'),
    pytest.param('combined', r'斬紅|蒼突|紫打|遠翠', id='alt-combined'),
])
def test_attr_alt_re(field, expected):
    from horsaga.data import AtkAttr
    assert AtkAttr.alternation_re(field) == expected

#
# Test: EnumMultiValueMixin with whitelisted / ignored fields
#

_fields = namedtuple('_MyFields', ('attr1', 'attr2', 'attr3', 'attr4'))

class ModFour(EnumMultiValueMixin, _fields, enum.Enum, lookup_enable=('attr1', 'attr3')):
    ZERO  = (0, 4,  8, 'doh')
    ONE   = (1, 5,  9, 'doh')
    TWO   = (2, 6, 10, 'doh')
    THREE = (3, 7, 11, 'doh')

@pytest.mark.skipif(sys.version_info < (3, 9, 2), reason='Feature requires Py 3.9.2+')
def test_multivalue_include():
    assert ModFour(1) == ModFour.ONE
    assert ModFour(9) == ModFour.ONE
    with pytest.raises(ValueError):
        ModFour(5)
    with pytest.raises(ValueError):
        ModFour('doh')

class ModFourAlt(EnumMultiValueMixin, _fields, enum.Enum, lookup_disable=('attr3', 'junk')):
    ZERO  = (0, 4,  8, 'doh')
    ONE   = (1, 5,  9, 'doh')
    TWO   = (2, 6, 10, 'doh')
    THREE = (3, 7, 11, 'doh')

@pytest.mark.skipif(sys.version_info < (3, 9, 2), reason='Feature requires Py 3.9.2+')
def test_multivalue_exclude():
    assert ModFourAlt(1) == ModFourAlt.ONE
    assert ModFourAlt(5) == ModFourAlt.ONE
    with pytest.raises(ValueError):
        ModFourAlt(9)
    # Last enum member wins, but we don't depend on such behavior
    # Generally such fields should be excluded instead
    assert isinstance(ModFourAlt('doh'), ModFourAlt)