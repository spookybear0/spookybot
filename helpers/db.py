from helpers.config import config
import aiomysql

async def connect_db(loop):
    global conn
    conn = await aiomysql.connect(host=config["sql_server"], port=config["sql_port"],
                                       user=config["sql_user"], password=config["sql_password"], db=config["sql_db"],
                                       loop=loop, connect_timeout=2880000)
    cursor = await conn.cursor()
    await cursor.execute("SET GLOBAL connect_timeout=2880000")
    await cursor.close()
    await conn.commit()
    return conn

async def add_user(username, user_id, content):
    cursor = await conn.cursor()
    
    await cursor.execute( # update user data
    """INSERT INTO `users`(username, id, latestmsg, lastbeatmap)
    VALUES (%s, %s, %s, '0')
    ON DUPLICATE KEY UPDATE latestmsg = %s;""",(username, user_id, content, content))
                    
    await cursor.close()
    await conn.commit()
    
async def log_command(username, user_id, content):
    cursor = await conn.cursor()
    await cursor.execute( # add log
    """INSERT INTO `logs`(username, id, log)
    VALUES (%s, %s, %s);""",(username, user_id, content))
                    
    await cursor.close()
    await conn.commit()
    
async def report_bug(username, user_id, bug):
    cursor = await conn.cursor()
    await cursor.execute( # report bug
    """INSERT INTO `bugreports`(bug, userid, username)
    VALUES (%s, %s, %s);""",(bug, user_id, username))
                    
    await cursor.close()
    await conn.commit()
    
async def add_suggestion(username, user_id, suggestion):
    cursor = await conn.cursor()
    await cursor.execute( # add suggestion
    """INSERT INTO `suggestions`(bug, userid, username)
    VALUES (%s, %s, %s);""",(suggestion, user_id, username))
                    
    await cursor.close()
    await conn.commit()
    
async def ban_user(username, user_id, reason):
    cursor = await conn.cursor()
    await cursor.execute( # ban user
    """INSERT INTO `bans`(username, id, reason)
    VALUES (%s, %s, %s);""",(username, user_id, reason))
                    
    await cursor.close()
    await conn.commit()
    
async def get_bugs():
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM bugreports;")
    
    result = await cursor.fetchall()
    
    await cursor.close()
    
    return result

async def get_suggestions():
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM suggestions;")
    
    result = await cursor.fetchall()
    
    await cursor.close()
    
    return result

async def get_users():
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM users;")
    
    result = await cursor.fetchall()
    
    await cursor.close()
    
    return result

async def set_last_beatmap(username, map_id):
    cursor = await conn.cursor()
    await cursor.execute( # ban user
    """UPDATE `users`
    SET lastbeatmap = %s
    WHERE username = %s;""",(map_id, username))
                    
    await cursor.close()
    await conn.commit()
    
async def remove_user(username=None, user_id=None):
    cursor = await conn.cursor()
    if username:
        await cursor.execute( # remove user by username
        """DELETE FROM `users`
        WHERE username = %s;""",(username))
    elif user_id:
        await cursor.execute( # remove user by id
        """DELETE FROM `users`
        WHERE id = %s;""",(user_id))
    else:
        raise ValueError("username or user_id argument must be filled in")
                    
    await cursor.close()
    await conn.commit()
    
async def unban_user(username=None, user_id=None):
    cursor = await conn.cursor()
    if username:
        await cursor.execute( # unban by username
        """DELETE FROM `bans`
        WHERE username = %s;""",(username))
    elif user_id:
        await cursor.execute( # unban by id
        """DELETE FROM `bans`
        WHERE id = %s;""",(user_id))
    else:
        raise ValueError("username or user_id argument must be filled in")
                    
    await cursor.close()
    await conn.commit()
    
async def get_last_beatmap(username):
    cursor = await conn.cursor()
    await cursor.execute("SELECT lastbeatmap FROM users WHERE username = %s;",(username))
    
    result = await cursor.fetchall()
    
    await cursor.close()
    
    return result

async def get_banned(username):
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM bans WHERE username = %s;",(username))
    
    result = await cursor.fetchall()
    
    await cursor.close()
    
    if result: return True
    return False

async def get_logs():
    cursor = await conn.cursor()
    await cursor.execute("SELECT log FROM logs;")
    
    result = await cursor.fetchall()
    
    await cursor.close()
    
    return result