import unittest
import asyncio
from commands import rank, github, help, ping, pp, recent, top, user
from helpers.config import load_config
import warnings

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Test(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        return super().setUp()

class TestGithub(Test):
    
    def test_github(self):
        r = asyncio.run(github.github({}, ["!github"]))
        self.assertEqual(r, "https://github.com/spookybear0/spookybot.")
        
class TestHelp(Test):
    def test_help(self):
        r = asyncio.run(help.help({}, ["!help"]))
        self.assertEqual(r, "https://github.com/spookybear0/spookybot/wiki/Command-list.")
        
class TestPing(Test):
    def test_ping(self):
        r = asyncio.run(ping.ping({}, ["!ping"]))
        self.assertEqual(r, "Pong!")

# no real testing (yet)

class TestPP(Test):
    def test_if_fail(self):
        try:
            r = asyncio.run(pp.pp({}, ["!pp", "1236756"]))
        except Exception as e:
            self.fail(e)
        
# recent can't have real tests as it depends on a recent play

class TestRecent(Test):
    def test_if_fail(self): # triple check for recent plays
        exc = ""
        succeded = False
        for username in ["sakamata1", "spookybear0", "WhiteCat", "BTMC", "Utami", "Reedkatt"]:
            try:
                asyncio.run(recent.recent({}, ["!recent", username]))
            except Exception as e:
                exc = e
            else: # 1 succeded
                succeded = True
        
        if not succeded:
            self.fail(e)
                

# top play test will be made later (maybe I will use peppys)

class TestTop(Test):
    def test_if_fail(self):
        try:
            r = asyncio.run(top.top({}, ["!top", "1", "WhiteCat"]))
        except Exception as e:
            self.fail(e)
            
# user can't have real tests as it depends on a pp (unless they are offline forever)

class TestUser(Test):
    def test_if_fail(self):
        try:
            r = asyncio.run(user.user({}, ["!user", "peppy"]))
        except Exception as e:
            self.fail(e)

if __name__ == '__main__':
    try:
        load_config()
    except SystemExit:
        exit(1)
        
    try:
        unittest.main()
    except RuntimeError:
        pass