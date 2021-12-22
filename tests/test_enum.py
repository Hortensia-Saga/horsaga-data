#
# Test: EnumMultiValueMixin works for enums
#

from random import choice

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
