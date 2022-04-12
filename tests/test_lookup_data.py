#
# Test: lookup() methods of various structure
#

import re

import pytest

from horsaga.data import CardBase, Character, Enchant, Formation, Skill, Tactic


@pytest.mark.parametrize(('lookup_arg', 'expected'), [
    pytest.param(200001, Enchant.cache()[200001], id='by-id'),
    pytest.param('試金石の装衣', frozenset({Enchant.cache()[200001]}), id='by-name'),
    pytest.param(10, None, id='by-id-fail'),
    pytest.param('Junk', frozenset(), id='by-name-fail'),
])
def test_enchant_lookup(lookup_arg, expected):
    if hasattr(expected, '__iter__'):
        assert Enchant.lookup(lookup_arg) == expected
    else:
        assert Enchant.lookup(lookup_arg) is expected

def test_enchant_lookup_multi():
    result = Enchant.lookup('練気の装衣')
    assert hasattr(result, '__contains__')
    assert (
        Enchant.cache()[100017] in result and
        Enchant.cache()[100044] in result
    )


@pytest.mark.parametrize(('lookup_arg', 'expected'), [
    pytest.param(111, Formation.cache()[111], id='by-id'),
    pytest.param('オーベルソウル★0', Formation.cache()[111], id='by-name'),
    pytest.param(30, None, id='by-id-fail'),
])
def test_formation_lookup(lookup_arg, expected):
    assert Formation.lookup(lookup_arg) is expected


@pytest.mark.parametrize(('lookup_arg', 'expected'), [
    pytest.param(110116, Skill.cache()[110116], id='by-id'),
    pytest.param('遠翠の天威', frozenset({Skill.cache()[110129]}), id='by-name'),
    pytest.param('NORMAL_ATTACK_DAMAGE_UP', frozenset({
        Skill.cache()[111005],
        Skill.cache()[111006],
    }), id='by-code'),
    pytest.param(1234567, None, id='by-id-fail'),
    pytest.param('Junk', frozenset(), id='by-str-fail'),
])
def test_skill_lookup(lookup_arg, expected):
    if hasattr(expected, '__iter__'):
        assert Skill.lookup(lookup_arg) == expected
    else:
        assert Skill.lookup(lookup_arg) is expected


def test_skill_lookup_pattern():
    pattern = re.compile(r'ATTACK\d_AT$')
    results = Skill.lookup(pattern)
    assert hasattr(results, '__contains__')
    for id in (122402, 126303, 127502):
        assert Skill.cache()[id] in results


@pytest.mark.parametrize(('lookup_arg', 'expected'), [
    pytest.param(30203, Tactic.cache()[30203], id='by-id'),
    pytest.param('エース／煌', frozenset({Tactic.cache()[40304]}), id='by-name'),
    pytest.param('HP_CURE', frozenset({
        Tactic.cache()[10101],
        Tactic.cache()[10102],
        Tactic.cache()[10103],
    }), id='by-code'),
    pytest.param(10, None, id='by-id-fail'),
    pytest.param('Junk', frozenset(), id='by-str-fail'),
])
def test_tactic_lookup(lookup_arg, expected):
    if hasattr(expected, '__iter__'):
        assert Tactic.lookup(lookup_arg) == expected
    else:
        assert Tactic.lookup(lookup_arg) is expected


def test_tactic_lookup_fail():
    pattern = re.compile(r'_CURE$')
    results = Tactic.lookup(pattern)
    assert hasattr(results, '__contains__')
    for id in (10202, 20103, 30702, 42403):
        assert Tactic.cache()[id] in results


@pytest.mark.parametrize(('lookup_arg', 'expected'), [
    pytest.param(1021, Character.cache()[1021], id='by-id'),
    pytest.param(999, None, id='by-id-fail'),
])
def test_chara_lookup(lookup_arg, expected):
    if hasattr(expected, '__iter__'):
        assert Character.lookup(lookup_arg) == expected
    else:
        assert Character.lookup(lookup_arg) is expected


@pytest.mark.parametrize(('lookup_arg', 'expected'), [
    pytest.param(1023, CardBase.cache()[1023], id='by-id'),
    pytest.param(999, None, id='by-id-fail'),
])
def test_card_lookup(lookup_arg, expected):
    if hasattr(expected, '__iter__'):
        assert CardBase.lookup(lookup_arg) == expected
    else:
        assert CardBase.lookup(lookup_arg) is expected
