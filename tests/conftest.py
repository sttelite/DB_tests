# -*- coding: utf-8 -*-
import pytest
import sqlite3
import shutil
import random
import os

ORIGINAL_DB = os.path.abspath("my_database.db")
TEMP_DB = "temp_database.db"


def randomize_parameters(data_dict):
    for name in data_dict:
        param_keys = list(data_dict[name].keys())
        chosen_param = random.choice(param_keys)
        # old_value = data_dict[name][chosen_param]
        data_dict[name][chosen_param] = random.choice(
            [i for i in range(1, 21)]
        )


@pytest.fixture(scope="session")
def generate_randomized_db():
    if os.path.exists(TEMP_DB):
        os.remove(TEMP_DB)
    shutil.copyfile(ORIGINAL_DB, TEMP_DB)

    original_conn = sqlite3.connect(ORIGINAL_DB)
    temp_conn = sqlite3.connect(TEMP_DB)

    original_cursor = original_conn.cursor()
    temp_cursor = temp_conn.cursor()

    original_cursor.execute("PRAGMA foreign_keys = ON")
    temp_cursor.execute("PRAGMA foreign_keys = ON")

    weapon_data = {}
    hull_data = {}
    engine_data = {}

    temp_cursor.execute(
        "SELECT weapon, reload_speed, rotational_speed, "
        "diameter, power_volley, count "
        "FROM weapons")
    rows = temp_cursor.fetchall()
    for row in rows:
        weapon_data[row[0]] = {
            "reload_speed": row[1],
            "rotational_speed": row[2],
            "diameter": row[3],
            "power_volley": row[4],
            "count": row[5],
        }
    randomize_parameters(weapon_data)

    temp_cursor.execute("SELECT hull, armor, type, capacity FROM hulls")
    rows = temp_cursor.fetchall()
    for row in rows:
        hull_data[row[0]] = {
            "armor": row[1],
            "type": row[2],
            "capacity": row[3],
        }
    randomize_parameters(hull_data)

    temp_cursor.execute("SELECT engine, power, type FROM engines")
    rows = temp_cursor.fetchall()
    for row in rows:
        engine_data[row[0]] = {
            "power": row[1],
            "type": row[2],
        }
    randomize_parameters(engine_data)

    for name, params in weapon_data.items():
        temp_cursor.execute('''
            UPDATE weapons SET
                reload_speed = ?, rotational_speed = ?, diameter = ?,
                            power_volley = ?, count = ?
            WHERE weapon = ?
        ''', (params["reload_speed"], params["rotational_speed"],
              params["diameter"], params["power_volley"],
              params["count"], name))

    for name, params in hull_data.items():
        temp_cursor.execute('''
            UPDATE hulls SET
                armor = ?, type = ?, capacity = ?
            WHERE hull = ?
        ''', (params["armor"], params["type"], params["capacity"], name))

    for name, params in engine_data.items():
        temp_cursor.execute('''
            UPDATE engines SET
                power = ?, type = ?
            WHERE engine = ?
        ''', (params["power"], params["type"], name))

    temp_conn.commit()
    yield original_cursor, temp_cursor
    original_conn.close()
    temp_conn.close()
    if os.path.exists(TEMP_DB):
        os.remove(TEMP_DB)
