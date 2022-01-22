#
# Test: Compare our data with official gacha data
#

from horsaga.data import CardBase


def test_comparedata(gacha_data):
    ids_from_db = {i for i in CardBase._cache.keys() if i < 5000}
    assert ids_from_db == gacha_data.keys()

    for id in ids_from_db:
        # assemble rows from our data
        card = CardBase.lookup(id)
        my_row = [
            card.rare.name,
            card.bp,
            card.title,
            card.hp,
            card.attack,
            card.defend,
            card.speed.value,
        ]

        if card.chara is not None:
            # TODO need to implement hero flag
            if card.chara.name == '@@@':
                my_row[2] += '主人公'
            else:
                my_row[2] += card.chara.name

        for attr_name in ['skill', 'uf']:
            if (attr := getattr(card, attr_name)):
                my_row.extend([attr.name, attr.desc])
            else:
                my_row.extend([None, None])

        for pos in (0, 1):
            try:
                tactic = card.tactic[pos]
            except IndexError:
                my_row.append(None)
            else:
                my_row.append(tactic.id)

        if card.enchant is None:
            my_row.append(None)
        else:
            my_row.append(card.enchant.name)

        gacha_row = gacha_data[id]
        # Data retrieval still unfinished, we skip some fields
        _ = gacha_row.pop(0) # attr
        assert my_row == gacha_row
