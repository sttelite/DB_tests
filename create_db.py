# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect("my_database.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS weapons (
        weapon TEXT PRIMARY KEY,
        reload_speed INTEGER,
        rotational_speed INTEGER,
        diameter INTEGER,
        power_volley INTEGER,
        count INTEGER
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS hulls (
        hull TEXT PRIMARY KEY,
        armor INTEGER,
        type INTEGER,
        capacity INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS engines (
        engine TEXT PRIMARY KEY,
        power INTEGER,
        type INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ships (
        ship TEXT PRIMARY KEY,
        weapon text,
        hull text,
        engine text,
        FOREIGN KEY (weapon) REFERENCES weapons(weapon),
        FOREIGN KEY (hull) REFERENCES hulls(hull),
        FOREIGN KEY (engine) REFERENCES engines(engine)
    )
''')
