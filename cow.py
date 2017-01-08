import logging
import asyncio
import random

import vertica_python


logging.getLogger('asyncio').setLevel(logging.WARNING)

async def setup(loop):
    conn = vertica_python.connect(**conn_info, loop=loop)
    await conn.startup_connection()
    cur = conn.cursor()
    await cur.execute('ALTER DATABASE mydb SET MaxClientSessions = 1000;')
    res = await cur.fetchone()


async def vtest(loop, val):
    conn_info = {
        'host': 'localhost',
        'port': 5433,
        'user': 'dbadmin',
        'password': 'cow',
        'database': 'docker',
        'read_timeout': '300',
        'autoconnect': True}

    try:
        conn = vertica_python.connect(**conn_info, loop=loop)
        await conn.startup_connection()
        cur = conn.cursor()
        await cur.execute("select %s as cow;" % val)
        res = await cur.fetchone()
        #await cur.execute("select 123 as cow;")
        #xx = await cur.fetchone()
        return res
    except Exception as exc:
        print("Got %r" % exc)

loop = asyncio.get_event_loop()

coros = []
for x in range(400):
    coros.append(asyncio.ensure_future(vtest(loop, random.randint(0, 1000))))
res = asyncio.gather(*coros)


#loop.set_debug(enabled=True)
loop.run_until_complete(res)
print(res)
loop.close()

