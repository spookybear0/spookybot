from helpers.config import config
import aiomysql

async def connect_db(loop):
    global conn
    conn = await aiomysql.connect(host=config["sql_server"], port=config["sql_port"],
                                       user=config["sql_user"], password=config["sql_password"], db=config["sql_db"],
                                       loop=loop)
    return conn

async def add_user(username, user_id, content):
    cursor = await conn.cursor()
    cursor.execute( # update user data
    """INSERT INTO `users`(username, id, latestmsg)
    VALUES (%s, %s, 1, %s);""",(username, user_id, content))
                    
    await cursor.close()
    await conn.commit()
    
async def log_command(username, user_id, content):
    cursor = await conn.cursor()
    cursor.execute( # add log
    """INSERT INTO `logs`(username, id, log)
    VALUES (%s, %s, %s);""",(username, user_id, content))
                    
    await cursor.close()
    await conn.commit()
    
async def report_bug(username, user_id, bug):
    cursor = await conn.cursor()
    cursor.execute( # report bug
    """INSERT INTO `bugreports`(bug, userid, username)
    VALUES (%s, %s, %s);""",(bug, user_id, username))
                    
    await cursor.close()
    await conn.commit()
    
async def add_suggestion(username, user_id, suggestion):
    cursor = await conn.cursor()
    cursor.execute( # add suggestion
    """INSERT INTO `suggestions`(bug, userid, username)
    VALUES (%s, %s, %s);""",(suggestion, user_id, username))
                    
    await cursor.close()
    await conn.commit()
    
async def ban_user(username, user_id, reason):
    cursor = await conn.cursor()
    cursor.execute( # ban user
    """INSERT INTO `bans`(username, id, reason)
    VALUES (%s, %s, %s);""",(username, user_id, reason))
                    
    await cursor.close()
    await conn.commit()
    
async def get_bugs():
    cursor = await conn.cursor()
    cursor.execute("SELECT * FROM bugreports;")
    
    result = cursor.fetchall()
    
    await cursor.close()
    
    return result

async def get_suggestions():
    cursor = await conn.cursor()
    cursor.execute("SELECT * FROM suggestions;")
    
    result = cursor.fetchall()
    
    await cursor.close()
    
    return result