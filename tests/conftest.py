import csv
from pathlib import Path

import pytest


@pytest.fixture
def gacha_data():
    csv_file = Path(__file__).parent / 'gacha_data.csv'
    resultset = {}
    with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            converted = []
            for v in row:
                if len(str(v)):
                    try:
                        v = int(v)
                    except ValueError:
                        pass
                    converted.append(v)
                else:
                    converted.append(None)
            id = converted.pop(0)
            resultset[id] = converted
    return resultset
