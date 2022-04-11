#
# Recursively scan folder for PvP related JSON files
# and retrieve card ID <--> character ID mapping
#

import json
import sys
from pathlib import Path


def dir_walker(path: Path):
    for child in path.iterdir():
        if child.is_file():
            yield child
        else:
            for item in dir_walker(child):
                yield item

result = {}

for file in dir_walker(Path(sys.argv[1])):
    j = None
    with file.open() as f:
        try:
            j = json.load(f)
        except json.JSONDecodeError:
            continue
    if 'units_info' not in j:
        continue
    for unit in j['units_info']:
        cid = unit['card_id']
        chid = unit['char_id']
        if cid not in result:
            result[cid] = chid
        else:
            if result[cid] != chid:
                print(f'WARNING: card {cid} was mapped to char {result[cid]}, '
                    f'but {file} contains mapping to char {chid} instead', file=sys.stderr)

for k, v in result.items():
    print(f'{k}:{v}')