#
# Test: EnumMultiValueMixin works for enums
#

from random import choice

import pytest


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
