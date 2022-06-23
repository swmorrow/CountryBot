import pickle, sqlite3
from typing import List, Union
from contextlib import closing

from countrybot.configparser import DATABASE
from countrybot.rpdate import RPDate

from .excepts import ChannelNotSetError, DateNotSetError


### Guild IO Functions ###

def get_guilds() -> List[Union[int, None]]:
    """Gets list of guilds saved in the database"""
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:
            
            cur = cur.execute('''SELECT guild_id FROM Guilds;''')
            guilds = cur.fetchall()

    return [guild[0] for guild in guilds]

def register(guild_id: int) -> None:
    """Registers guild to database"""
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur.execute('''INSERT INTO Guilds (guild_id, rpdate, rpdate_channel)
                           VALUES((?), NULL, NULL);''',
                           (guild_id,))
            con.commit()
    
def unregister(guild_id: int) -> None:
    """Unregisters guild from database"""
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur.execute('''DELETE FROM Guilds
                           WHERE guild_id = (?);''',
                           (guild_id,))
            con.commit()


### RPDate IO Functions ###

def load_rpdate(guild_id: int) -> RPDate:
    """Loads RP date from database"""
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur = cur.execute('''SELECT rpdate FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = cur.fetchone()
            
    if not row[0]:
        raise DateNotSetError

    rpdate = pickle.loads(row[0])
    return rpdate

def save_rpdate(rpdate: RPDate, guild_id: int) -> None:
    """Serializes RPDate and saves it to the database """
    if rpdate:
        rpdate = pickle.dumps(rpdate)

    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur.execute('''UPDATE Guilds
                           SET rpdate = (?)
                           WHERE guild_id = (?);''',
                           (rpdate, guild_id))
            con.commit()

### Channel IO Functions ###

def save_rpdate_channel(rpdate_channel, guild_id: int) -> None:
    """Saves RPDate channel to the database """
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur.execute('''UPDATE Guilds
                           SET rpdate_channel = (?)
                           WHERE guild_id = (?);''',
                           (rpdate_channel, guild_id))
            con.commit()
    if rpdate_channel:
        print(f"RPDate channel {rpdate_channel} saved to {guild_id}.")
        return
    print(f"RPDate channel deleted from {guild_id}.")


def load_rpdate_channel(guild_id: int) -> int:
    """Loads RP date channel from database"""
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur = cur.execute('''SELECT rpdate_channel FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = cur.fetchone()
    if not row[0]:
        raise ChannelNotSetError

    return row[0]

def save_approve_channel(approval_channel, guild_id: int) -> None:
    """Saves approval queue channel to the database """
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur.execute('''UPDATE Guilds
                           SET approve_channel = (?)
                           WHERE guild_id = (?);''',
                           (approval_channel, guild_id))
            con.commit()
    if approval_channel:
        print(f"Approval channel {approval_channel} saved to {guild_id}.")
        return
    print(f"Approval channel deleted from {guild_id}.")

def load_approve_channel(guild_id: int) -> int:
    """Loads RP date channel from database"""
    with sqlite3.connect(DATABASE) as con:
        with closing(con.cursor()) as cur:

            cur = cur.execute('''SELECT approve_channel FROM Guilds
                                 WHERE guild_id = (?);''',
                                 (guild_id,))

            row = cur.fetchone()
    if row[0] is None:
        raise ChannelNotSetError

    return row[0]