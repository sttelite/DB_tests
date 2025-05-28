# -*- coding: utf-8 -*-
import sqlite3
import random

conn = sqlite3.connect("my_database.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("DELETE FROM Ships")
cursor.execute("DELETE FROM weapons")
cursor.execute("DELETE FROM hulls")
cursor.execute("DELETE FROM engines")
conn.commit()

for i in range(1, 21):
    name = f"weapon-{i}"
    reload_speed = random.randint(1, 20)
    rotational_speed = random.randint(1, 20)
    diameter = random.randint(1, 20)
    power_volley = random.randint(1, 20)
    count = random.randint(1, 20)
    cursor.execute('''
    INSERT INTO weapons (weapon, reload_speed, rotational_speed,
                    diameter, power_volley, count)
    VALUES (?, ?, ?, ?, ?, ?)
''', (name, reload_speed, rotational_speed, diameter, power_volley, count))

for i in range(1, 6):
    name = f"hull-{i}"
    armor = random.randint(1, 20)
    type = random.randint(1, 20)
    capacity = random.randint(1, 20)
    cursor.execute('''
    INSERT INTO hulls (hull, armor, type, capacity)
    VALUES (?, ?, ?, ?)
''', (name, armor, type, capacity))

for i in range(1, 7):
    name = f"engine-{i}"
    power = random.randint(1, 20)
    type = random.randint(1, 20)
    cursor.execute('''
    INSERT INTO engines (engine, power, type)
    VALUES (?, ?, ?)
''', (name, power, type))


for i in range(1, 201):
    name = f"Ship-{i}"
    i_weapon = random.randint(1, 20)
    i_hull = random.randint(1, 5)
    i_engine = random.randint(1, 6)
    cursor.execute('''
    INSERT INTO Ships (ship, weapon, hull, engine)
    VALUES (?, ?, ?, ?)
''', (name, f"weapon-{i_weapon}", f"hull-{i_hull}", f"engine-{i_engine}"))

conn.commit()
