import sqlite3
import util

db = None

def init():
	global db
	db = sqlite3.connect('database')
	db.row_factory = _dict_factory
	try:
		cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='champion';")
		if cursor.fetchall() == []:
			with open('src/queries/database.sql') as file:
				db.executescript(file.read())
	except Exception as e:
		print(str(e))

def terminate():
	global db
	db.commit()
	db.close()
	db = None

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select(query: str, params: dict = None):
	data = db.execute(query, params).fetchall()
	return data

def execute(query: str, params: dict = None):
	db.execute(query, params).fetchall()

def commit():
	db.commit()
