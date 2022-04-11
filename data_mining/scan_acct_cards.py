import csv

from horsaga import HorSaga, account
from horsaga.data import AtkAttr, horsaga_db
from horsaga.model.pagename import Page

players = [HorSaga(ac, login=False) for ac in account.enumerate()]

chara_data = {}
card_mapping = {}
url = Page('card', 'GetUserCardCollectionPage')

for p in players:
    for attr in list(AtkAttr):
        payload = {'attr': 'filter_' + attr.name.lower()}
        with p._ua.post(url, json=payload) as resp:
            for chara_obj in resp.parsed:
                if chara_obj.id not in chara_data:
                    chara_data[chara_obj.id] = (chara_obj.name, chara_obj.attr)
                for card_id in chara_obj.cards:
                    if card_id not in card_mapping:
                        card_mapping[card_id] = chara_obj.id

#
# Write character data
#

our_chara_ids = chara_data.keys()
resultset = horsaga_db.execute('SELECT id FROM chara')
db_chara_ids = {row[0] for row in resultset}

with open('extra_chara.txt', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(('id', 'name', 'attr'))
    for id in our_chara_ids - db_chara_ids:
        row = (id, chara_data[id][0], chara_data[id][1].name)
        writer.writerow(row)
    print('Extra character data written into extra_chara.txt')

#
# Write card ID -> character ID mapping
#
our_card_ids = card_mapping.keys()
resultset = horsaga_db.execute('SELECT id FROM cardbase WHERE chara IS NOT NULL')
db_card_ids = {row[0] for row in resultset}

with open('card_chara_map.txt', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(('id', 'chara'))
    for id in our_card_ids - db_card_ids:
        row = (id, card_mapping[id])
        writer.writerow(row)
    print('Extra (Card -> Character) mapping written into card_chara_map.txt')
