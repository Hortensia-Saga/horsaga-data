#
# Scrap most basic card data from gacha result
#
# It can also retrieve fake card like story bosses and internal
# card helpers etc, as long as card ID can be found.
# Note that character data and enchant data are absent.
#

from typing import Iterator, List
from random import choice

from lxml.html import document_fromstring
from lxml.cssselect import CSSSelector
from lxml.etree import XPath

from more_itertools.more import padded
from more_itertools.recipes import take

from horsaga import HorSaga, account
from horsaga._parser import scrap_text
from horsaga.model.url import CardImgUrl, TacticsIconUrl
from horsaga.model.pagename import Page

# Card ID to be skipped, some may not be released yet or never did
SKIPPED = (
    # 1437,
    1622,
    1623,
    2162,
    2485,
    2532,
)
START = 2529
END = 2537

payload = {
    'gcty': 'GOLD_10_FREE_FOR_CAMPAIGN', # Any valid param is fine
    'gccnt': '0',
    'gbucc': '450',
    'gccdo': 'true',
    'gsttf': 'true',
}

param_strs = [
    'prmImg',
    'prmAttribute',
    'prmRare',
    'prmBp',
    'prmName',
    'prmHp',
    'prmAtt',
    'prmDef',
    'prmSpe',
    'prmSkill',
    'prmSkillDetail',
    'prmSkill2',
    'prmSkillDetail2',
    'prmImgTac',
    'prmImgTac2',
    'enchantName'
]

selectors = [CSSSelector('span.' + v) for v in param_strs]

cards_xpath = XPath('//li[@data-id="gachaPopupCardDetail"]')

def card_id_gen(start, end) -> Iterator[int]:
    for i in range(start, end):
        if i not in SKIPPED:
            yield i

def gprcd_gen(start, end) -> Iterator[List[int]]:

    id_gen = card_id_gen(start, end)

    while (grp := take(10, id_gen)):
        if len(grp) < 10:
            grp = list(padded(grp, grp[-1], 10))
        yield grp


player = HorSaga(choice(account.enumerate()))

with open('gacha_data.csv', 'a', newline=None) as f:

    for gprcd in gprcd_gen(START, END):

        payload['gprcd'] = ','.join(str(v) for v in gprcd)

        resp = player._ua.get(
            Page('gacha', 'GachaResultPage'),
            params=payload,
            allow_redirects=False)

        tree = document_fromstring(resp.text)
        cards = cards_xpath(tree)
        assert isinstance(cards, list)

        prev = None
        if len(cards) > 0:
            for c in cards:
                data = scrap_text(c, selectors, default='')
                if prev == data[0]:
                    continue  # skip padding in gprcd_gen()
                else:
                    prev = data[0]

                formatted = [(str(d) if d else '') for d in data]

                if data[0]:
                    card_url = CardImgUrl.parse(data[0])
                    formatted[0] = str(card_url.id)
                    # SPECIAL: The only card with hero2_flag, which is
                    # impossible to obtain via gacha, has wrong BP
                    if card_url.id == 2093:
                        formatted[3] = '0'
                    # SPECIAL: Whitespace not cleaned up properly
                    if card_url.id == 1151:
                        formatted[4] = formatted[4].replace(' ', '')

                for pos in (-2, -3):
                    if data[pos]:
                        icon_url = TacticsIconUrl.parse(data[pos])
                        formatted[pos] = str(icon_url.id)

                formatted[-1] = formatted[-1].replace('未装備', '')

                print(','.join(formatted), file=f)
        else:
            print(f'{gprcd} Failed')
