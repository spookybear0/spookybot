import re
from helpers.parse import parse_args
from helpers.command import prefix, is_owner
from traceback import print_exc
from dataclasses import dataclass
import asyncio

modes = {
    "osu": 0,
    "taiko": 1,
    "ctb": 2,
    "mania": 3
}

@dataclass
class Player:
    username: str
    slot: int
    host: bool
    map_queued: int

@is_owner
async def say(ctx, args):
    await ctx.match.sendMultiMessage(" ".join(args[1:]))

@is_owner
async def eval(ctx, args):
    env = {
            "bot": ctx.bot,
            "irc": ctx.bot,
            "ctx": ctx,
            "msg": ctx.msg,
            "match": ctx.match,
            "send": ctx.match.sendMultiMessage
    }
    command = " ".join(args[1:])
    
    to_compile = f"import asyncio\nasync def func():\n    {command}\n\nout = asyncio.create_task(func())"
    
    #print(to_compile)
    
    try:
        exec_locals = {}
        exec(to_compile, env, exec_locals)
    except Exception as e:
        print_exc()
    else:
        out = exec_locals["out"]
        
        await out
        
        if out.result():
            await ctx.match.sendMultiMessage(out.result())
      
async def add(ctx, args):
    map = args[1]
    if re.match(r"https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#.*\/[0-9]+", map):
        mode, map_id = re.findall(r"https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#(.*)\/([0-9]+)", map)[0]
        map_id = int(map_id)
        if mode != "osu":
            await ctx.match.sendMultiMessage("Only osu! is supported")
            return
    else:
        map_id = int(map)
        mode = 0
    
    if ctx.username in ctx.match.queue_user:
        await ctx.match.sendMultiMessage(f"You ({ctx.username}) have already added a map to the queue!")
        return
    
    if map_id in ctx.match.queue_map: # already in queue
        await ctx.match.sendMultiMessage(f"{map_id} is already in the queue!")
        return
    
    ctx.match.queue_map.append(map_id)
    ctx.match.queue_user.append(ctx.username)
    
    await ctx.match.sendMultiMessage(f"{map_id} added to queue!")

async def skip(ctx, args):
    ctx.match.skip = True
    ctx.match.played_map = True
    await ctx.match.sendMultiMessage(f"Skipping map! In the future this will require a vote.")
    await ctx.match.sendMultiCommand("aborttimer")
    
@is_owner
async def force_skip(ctx, args):
    ctx.match.skip = True
    ctx.match.played_map = True
    await ctx.match.sendMultiMessage(f"Force skipped!")
    await ctx.match.sendMultiCommand("aborttimer")
    
async def info(ctx, args):
    await ctx.match.sendMultiMessage(f"Use !add (map id or link) to add a map to the queue, Use !help for more info.")
    
async def queue(ctx, args):
    if not ctx.username in ctx.match.queue_user:
        await ctx.match.sendMultiMessage("You are not in the queue.")
        return
    ind = ctx.match.queue_user.index(ctx.username)
    if ind == 0:
        await ctx.match.sendMultiMessage(f"Your map is being played now.")
    else:
        await ctx.match.sendMultiMessage(f"Your map will be played after {ind} more maps.")

commands = {
            "say": {"handler": say, "aliases": []},
            "exec": {"handler": eval, "aliases": ["eval"]},
            "add": {"handler": add, "aliases": ["add_map", "a"]},
            "skip": {"handler": skip, "aliases": ["s"]},
            "forceskip": {"handler": force_skip, "aliases": ["fs"]},
            "info": {"handler": info, "aliases": ["i"]},
            "queue": {"handler": queue, "aliases": ["q"]}
            }

class Match:
    def __init__(self, irc, mp_id: int, room_name: str):
        self.irc = irc
        self.mp_id = mp_id
        self.room_name = room_name
        
        self.password = True
        self.slots = {}
        self.queue_map = []
        self.queue_user = []
        self.current_map = None
        self.in_progress = False
        self.timer_started = False
        self.played_map = True
        self.no_maps_in_queue_alert = True
        self.skip = False
        
    @classmethod
    async def create(cls, irc, mp_id: int, room_name: str):
        ret = cls(irc, mp_id, room_name)
        await ret.onReady()
        return ret
    
    def get_username_from_slot(self, slot: int):
        return self.slots[slot]
    
    def get_slot_from_username(self, username: str):
        return list(self.slots.keys())[list(self.slots.values()).index(username)]
    
    async def loop(self):
        while True:
            if (not self.in_progress and self.played_map and not self.timer_started) or self.skip:
                if self.skip:
                    self.skip = False
                    self.in_progress = False
                    self.played_map = True
                    self.timer_started = False
                    self.queue_map.pop(0)
                    self.queue_user.pop(0)
                try:
                    map = self.queue_map[0]
                except IndexError:
                    if self.no_maps_in_queue_alert:
                        await self.sendMultiMessage("No maps in queue! Add a map with !add.")
                        self.no_maps_in_queue_alert = False
                else:
                    self.no_maps_in_queue_alert = True
                    self.played_map = False
                    await self.sendMultiMessage(f"Changing map to {map}.")
                    await self.changeMap(map)
                    await asyncio.sleep(0.5)
                    await self.sendMultiMessage("Starting match timer.")
                    await self.startMatch(60)
            
            await asyncio.sleep(0.1)
    
    async def sendMultiMessage(self, message):
        return await self.irc.sendMessage(f"mp_{self.mp_id}", message) # remove password

    async def sendMultiCommand(self, command):
        return await self.irc.sendMessage(f"mp_{self.mp_id}", f"!mp {command}") # remove password
    
    async def changeMap(self, map_id: int):
        self.current_map = map_id
        return await self.sendMultiCommand(f"map {map_id} 0")
    
    async def startMatch(self, timer: int=0):
        self.timer_started = True
        return await self.sendMultiCommand(f"start {timer}")
    
    async def onReady(self):
        await self.irc.joinChannel(f"mp_{self.mp_id}") # join irc channel
        
        await self.sendMultiCommand("password") # remove password
        await self.sendMultiCommand("mods Freemod") # add Freemod
        
        asyncio.get_event_loop().create_task(self.loop())
        
    async def onMessage(self, ctx):
        msg = ctx.msg
        args = parse_args(ctx.content)
        if args[0].startswith(prefix):
            args.insert(0, args[0].replace(prefix, ""))
            args.pop(1)
            for name, info in commands.items():
                if args[0] == name:
                    try:
                        await info["handler"](ctx, args)
                    except Exception as e:
                        print(f"Error in command {name}.")
                        print_exc()
            for alias in info["aliases"]:
                if args[0] == alias:
                    try:
                        await info["handler"](ctx, args)
                    except Exception as e:
                        print(f"Error in command {name}.")
                        print_exc()
                continue
        #print(msg.user_name, msg.content, self.mp_id, self.queue_map, self.queue_user)
        #elif re.match(r"is listening to \[https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#\/([0-9]+) .*\]", msg.content):
        #    map_id = re.findall(r"is listening to \[https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#\/([0-9]+) .*\]", msg.content)[0]
        #    print(map_id)
                    
    async def onMultiEvent(self, ctx): # commands for later use
        msg = ctx.msg
        content = msg.content
        
        if content == "Removed the match password":
            self.password = False
        elif content == "Changed the match password":
            self.password = True
        elif re.match(r"(.*) joined in slot (\d+)\.", content):
            username, slot = re.findall(r"(.*) joined in slot (\d+)\.", content)[0]
            slot = int(slot)
            self.slots[slot] = username
        elif re.match(r"(.*) left the game\.", content):
            username = re.findall(r"(.*) left the game\.", content)[0]
            self.slots.pop(self.get_slot_from_username(username))
        elif re.match(r"(.*) moved to slot (\d+)", content):
            username, slot = re.findall(r"(.*) moved to slot (\d+)", content)[0]
            slot = int(slot)
            self.slots.pop(self.get_slot_from_username(username))
            self.slots[slot] = username
        elif content == "The match has started!":
            self.in_progress = True
            self.timer_started = False
            self.queue_map.pop(0)
            self.queue_user.pop(0)
        elif content == "The match has finished!" or content == "Aborted the match":
            await asyncio.sleep(15)
            self.in_progress = False
            self.timer_started = False
            self.played_map = True
            
        #print(self.room_name, self.mp_id, msg.user_name, msg.content, self.queue_map, self.queue_user)