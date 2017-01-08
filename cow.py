import logging
import asyncio

import vertica_python


logging.getLogger('asyncio').setLevel(logging.WARNING)


async def request(val, cur):
   return res
    #print('%s\n' % await cur.fetchone())


async def vtest(loop, val):
    conn_info = {
        'host': 'localhost',
        'port': 5433,
        'user': 'dbadmin',
        'password': 'cow',
        'database': 'docker',
        'read_timeout': '300',
        'autoconnect': True}

    conn = vertica_python.connect(**conn_info, loop=loop)
    await conn.startup_connection()
    cur = conn.cursor()
    await cur.execute("select %s as cow;" % val)
    res = await cur.fetchone()
    #await cur.execute("select 123 as cow;")
    #xx = await cur.fetchone()
    return res

loop = asyncio.get_event_loop()

coros = [
    asyncio.ensure_future(vtest(loop, 123)),
    asyncio.ensure_future(vtest(loop, 345)),
    asyncio.ensure_future(vtest(loop, 456))]
res = asyncio.gather(*coros)

#loop.set_debug(enabled=True)
loop.run_until_complete(res)
print(res)
loop.close()

