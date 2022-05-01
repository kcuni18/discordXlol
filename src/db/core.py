import aiosqlite

db = None

async def init():
	global db
	db = await aiosqlite.connect('database')
	db.row_factory = _dict_factory
	data = await select('SELECT name FROM sqlite_master WHERE type="table" AND name="champion";')
	if len(data) == 0:
		with open('queries/database.sql') as file:
			await db.executescript(file.read())
		with open('queries/data.sql') as file:
			await db.executescript(file.read())
		await db.commit()

async def terminate():
	global db
	await db.commit()
	await db.close()
	db = None

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

async def select(query: str, params: dict = None) -> dict:
	cursor = await db.execute(query, params)
	data = await cursor.fetchall()
	await cursor.close()
	return data

async def execute(query: str, params: dict = None):
	await db.execute(query, params)

async def commit():
	await db.commit()


###### TESTING ######
import json
import asyncio

async def _test():
	try:
		await init()

		data = await select('SELECT * FROM summoners WHERE name="CapKunkka"')
		print(json.dumps(data))

		await terminate()
	except Exception as e:
		print(str(e))

if __name__ == '__main__':
	asyncio.run(_test())

