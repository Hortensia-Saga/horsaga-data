#
# Generates sqlite3 database for Hortensia Saga data
#

import csv
import sqlite3

from _common import RAW_DATA_DIR, SRC_DIR

DB_FILE_NAME = 'horsaga.sqlite3'
DB_BACKUP_NAME = DB_FILE_NAME + '.bak'

db_schema = {
    'ability_mat_type': '''
        "gid"   INTEGER,
        "type"  TEXT NOT NULL,
        PRIMARY KEY("gid")
    ''',
    'attack_attrib': '''
        "value"     INTEGER,
        "code"      TEXT NOT NULL,
        "kanji"     TEXT,
        "color"     TEXT,
        "combined"  TEXT,
        PRIMARY KEY("value")
    ''',
    'awaken_gain': '''
        "type"        TEXT    NOT NULL,
        "lvl1_hp"     INTEGER NOT NULL,
        "lvl1_atk"    INTEGER NOT NULL,
        "lvl1_def"    INTEGER NOT NULL,
        "lvl1_speed"  INTEGER NOT NULL,
        "lvl2_hp"     INTEGER NOT NULL,
        "lvl2_atk"    INTEGER NOT NULL,
        "lvl2_def"    INTEGER NOT NULL,
        "lvl2_speed"  INTEGER NOT NULL,
        "lvl3_hp"     INTEGER NOT NULL,
        "lvl3_atk"    INTEGER NOT NULL,
        "lvl3_def"    INTEGER NOT NULL,
        "lvl3_speed"  INTEGER NOT NULL,
        PRIMARY KEY("type")
    ''',
    'enchant': '''
        "id"       INTEGER,
        "name"     TEXT NOT NULL,
        "max_hp"   INTEGER,
        "max_atk"  INTEGER,
        "max_def"  INTEGER,
        PRIMARY KEY("id")
    ''',
    'rarity': '''
        "value"      INTEGER NOT NULL,
        "code"       TEXT    NOT NULL,
        "full_name"  TEXT    NOT NULL,
        PRIMARY KEY("value")
    ''',
    'formation': '''
        "id"         INTEGER NOT NULL,
        "name"       TEXT    NOT NULL UNIQUE,
        "desc"       TEXT    NOT NULL,
        "type"       INTEGER NOT NULL,
        PRIMARY KEY("id")
    ''',
    'skill': '''
        "id"    INTEGER,
        "code"  TEXT,
        "name"  TEXT NOT NULL UNIQUE,
        "desc"  TEXT NOT NULL,
        PRIMARY KEY("id")
    ''',
    'rank': '''
        "value"      INTEGER,
        "code"       TEXT NOT NULL UNIQUE,
        "min_hp"     INTEGER,
        "min_atk"    INTEGER,
        "min_def"    INTEGER,
        "min_speed"  INTEGER,
        PRIMARY KEY("value")
    ''',
    'tactic': '''
        "id"       INTEGER,
        "name"     TEXT NOT NULL UNIQUE,
        "desc"     TEXT NOT NULL,
        "code"     TEXT,
        "tp_cost"  INTEGER,
        PRIMARY KEY("id")
    ''',
    'chara': '''
        "id"                  INTEGER,
        "name"                TEXT NOT NULL,
        "cv"                  TEXT,
        "illust"              TEXT,
        "infotext"            TEXT,
        "attr"                INTEGER,
        "awaken_gain"         TEXT,
        "voice_self_intro"    TEXT,
        "voice_gacha"         TEXT,
        "voice_battle_start"  TEXT,
        "voice_battle_end"    TEXT,
        "voice_login"         TEXT,
        "voice_lvl_up"        TEXT,
        "voice_lvl_max"       TEXT,
        "voice_awaken"        TEXT,
        FOREIGN KEY("awaken_gain") REFERENCES "awaken_gain"("type"),
        FOREIGN KEY("attr"       ) REFERENCES "attack_attrib"("value"),
        PRIMARY KEY("id")
    ''',
    'cardbase': '''
        "id"        INTEGER,
        "title"     TEXT    NOT NULL,
        "hp"        INTEGER NOT NULL,
        "attack"    INTEGER NOT NULL,
        "defend"    INTEGER NOT NULL,
        "speed"     INTEGER NOT NULL,
        "bp"        INTEGER NOT NULL,
        "rare"      INTEGER NOT NULL,
        "chara"     INTEGER,
        "flag"      INTEGER NOT NULL DEFAULT 0,
        "skill"     INTEGER,
        "uf"        INTEGER CHECK("skill" IS NOT NULL OR "uf" IS NULL),
        "tactic1"   INTEGER,
        "tactic2"   INTEGER CHECK("tactic1" IS NOT NULL OR "tactic2" IS NULL),
        "enchant"   INTEGER,
        "kn_skill"  INTEGER CHECK(kn_skill BETWEEN 2000000 AND 2999999),
        PRIMARY KEY("id"),
        FOREIGN KEY("rare"    ) REFERENCES "rarity"("value"),
        FOREIGN KEY("tactic1" ) REFERENCES "tactic"("id"),
        FOREIGN KEY("tactic2" ) REFERENCES "tactic"("id"),
        FOREIGN KEY("enchant" ) REFERENCES "enchant"("id"),
        FOREIGN KEY("chara"   ) REFERENCES "chara"("id"),
        FOREIGN KEY("kn_skill") REFERENCES "skill"("id"),
        FOREIGN KEY("uf"      ) REFERENCES "skill"("id"),
        FOREIGN KEY("skill"   ) REFERENCES "skill"("id")
    ''',
}


def do_backup(file_loc, backup_loc):
    backup_loc.unlink(missing_ok=True)
    try:
        file_loc.rename(backup_loc)
    except FileNotFoundError:
        pass


def build(*, backup: bool = False):
    bkfile = SRC_DIR / DB_BACKUP_NAME
    dbfile = SRC_DIR / DB_FILE_NAME

    if backup:
        do_backup(dbfile, bkfile)
    else:
        dbfile.unlink(missing_ok=True)

    con = sqlite3.connect(dbfile)
    con.execute('PRAGMA foreign_keys = 1;')

    # Note: table order matters, some have foreign key constraints
    for tbl_name, tbl_struct in db_schema.items():
        with con:
            create_st = f'CREATE TABLE "{tbl_name}" ({tbl_struct})'
            con.execute(create_st)

        raw_data_file = RAW_DATA_DIR / f'{tbl_name}.csv'
        with con, open(raw_data_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            row_size = len(next(reader))
            insert_st = 'INSERT INTO "{}" VALUES ({})'.format(
                tbl_name, ', '.join(['?'] * row_size)
            )

            for row in reader:
                # csv reader produce string-only result, need conversion
                fixed_row = []
                for v in row:
                    if len(str(v)):
                        try:
                            v = int(v)
                        except ValueError:
                            pass
                        fixed_row.append(v)
                    else:
                        fixed_row.append(None)
                try:
                    con.execute(insert_st, fixed_row)
                except:
                    print(f'Failed at row ' + str(fixed_row))
                    raise

            # Special fake character IDs, many cards still don't have
            # corresponding character data discovered yet. Hopefully
            # this section can be removed in future
            if tbl_name == 'chara':
                data = [(i * 1000, '', i) for i in range(1, 5)]
                con.executemany(
                    'INSERT INTO "chara" (id, name, attr) VALUES (?, ?, ?)', data
                )

    con.close()


build()
