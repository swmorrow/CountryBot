import pickle, aiosqlite
import datetime as dt
from typing import List, Union
from contextlib import closing

from countrybot.configparser import DATABASE
from countrybot.rpdate import RPDate

from .excepts import ChannelNotSetError, DateNotSetError, RPDateNotPostedError


### Guild IO Functions ###

async def get_guilds() -> List[Union[int, None]]:
    """Gets list of guilds saved in the database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:
            
            cur = await cur.execute('''SELECT guild_id FROM Guilds;''')
            guilds = await cur.fetchall()

    return [guild[0] for guild in guilds]

async def register(guild_id: int) -> None:
    """Registers guild to database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            await cur.execute('''INSERT INTO Guilds (guild_id, rpdate, rpdate_channel)
                           VALUES((?), NULL, NULL);''',
                           (guild_id,))
            await con.commit()
    
async def unregister(guild_id: int) -> None:
    """Unregisters guild from database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            await cur.execute('''DELETE FROM Guilds
                           WHERE guild_id = (?);''',
                           (guild_id,))
            await con.commit()


### RPDate IO Functions ###

async def load_rpdate(guild_id: int) -> RPDate:
    """Loads RP date from database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            cur = await cur.execute('''SELECT rpdate FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = await cur.fetchone()
            
    if row[0] is None:
        raise DateNotSetError

    rpdate = pickle.loads(row[0])
    return rpdate

async def save_rpdate(rpdate: RPDate, guild_id: int) -> None:
    """Serializes RPDate and saves it to the database """
    if rpdate:
        rpdate = pickle.dumps(rpdate)

    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            await cur.execute('''UPDATE Guilds
                           SET rpdate = (?)
                           WHERE guild_id = (?);''',
                           (rpdate, guild_id))
            await con.commit()

async def save_last_rpdate_posting(date: dt.datetime, guild_id: int) -> None:
    """Saves the time of last rpdate posting for a guild in the database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            await cur.execute('''UPDATE Guilds
                           SET last_rpdate_posting = (?)
                           WHERE guild_id = (?);''',
                           (date, guild_id))
            await con.commit()

async def load_last_rpdate_posting(guild_id: int) -> dt.datetime:
    """Loads RP date from database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            cur = await cur.execute('''SELECT last_rpdate_posting FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = await cur.fetchone()
            
    if row[0] is None:
        raise RPDateNotPostedError

    return dt.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")

### Channel IO Functions ###

async def save_rpdate_channel(rpdate_channel: int, guild_id: int) -> None:
    """Saves RPDate channel to the database """
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            await cur.execute('''UPDATE Guilds
                           SET rpdate_channel = (?)
                           WHERE guild_id = (?);''',
                           (rpdate_channel, guild_id))
            await con.commit()

async def load_rpdate_channel(guild_id: int) -> int:
    """Loads RP date channel from database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            cur = await cur.execute('''SELECT rpdate_channel FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = await cur.fetchone()
            
    if row[0] is None:
        raise ChannelNotSetError("Date")

    return row[0]

async def save_approve_channel(approval_channel, guild_id: int) -> None:
    """Saves approval queue channel to the database """
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            await cur.execute('''UPDATE Guilds
                           SET approve_channel = (?)
                           WHERE guild_id = (?);''',
                           (approval_channel, guild_id))
            await con.commit()

async def load_approve_channel(guild_id: int) -> int:
    """Loads RP date channel from database"""
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cur:

            cur = await cur.execute('''SELECT approve_channel FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = await cur.fetchone()

    if row[0] is None:
        raise ChannelNotSetError("Claims")

    return row[0]