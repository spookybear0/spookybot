import unittest, asyncio, os
from commands import rank, github, help, ping, pp, recent, top, user
from ratelimiter import RateLimiter
        
class TestGithub(unittest.TestCase):
    def test_github(self):
        r = asyncio.run(github.github({}, ["!github"]))
        self.assertEqual(r, "The github page for this project can be found at https://github.com/spookybear0/spookybot.")
        
class TestHelp(unittest.TestCase):
    def test_help(self):
        r = asyncio.run(help.help({}, ["!help"]))
        self.assertEqual(r, "Check out the list of commands here: https://github.com/spookybear0/spookybot/wiki/Command-list.")
        
class TestPing(unittest.TestCase):
    def test_ping(self):
        r = asyncio.run(ping.ping({}, ["!ping"]))
        self.assertEqual(r, "Pong!")

# no real testing (yet)

class TestPP(unittest.TestCase):
    def test_if_fail(self):
        try:
            r = asyncio.run(pp.pp({}, ["!pp", "1236756"]))
        except Exception as e:
            self.fail(e)

class TestRank(unittest.TestCase):
    def test_manual_type_pp(self):
        r = asyncio.run(rank.rank({}, ["!rank", "100", "pp"], True))
        self.assertGreater(2023918, r)
        
    def test_manual_type_pp2(self):
        r = asyncio.run(rank.rank({}, ["!rank", "200pp", "pp"], True))
        self.assertGreater(1503935, r)
        
    def test_manual_type_pp_str(self):
        r = asyncio.run(rank.rank({}, ["!rank", "1k", "pp"], True))
        self.assertGreater(573709, r)
        
    def test_manual_type_pp_str2(self):
        r = asyncio.run(rank.rank({}, ["!rank", "1kpp", "pp"], True))
        self.assertGreater(573709, r)
    
    def test_manual_type_rank(self):
        r = asyncio.run(rank.rank({}, ["!rank", "300k", "rank"], True))
        self.assertGreater(1971, r)
        
    def test_manual_type_rank2(self):
        r = asyncio.run(rank.rank({}, ["!rank", "300000", "rank"], True))
        self.assertGreater(1971, r, 1000)
        
    def test_rank_str(self):
        r = asyncio.run(rank.rank({}, ["!rank", "1k"], True))
        self.assertGreater(10492, r, 1000)
        
    def test_rank_pp_str(self):
        r = asyncio.run(rank.rank({}, ["!rank", "1kpp"], True))
        self.assertGreater(573709, r, 1000)
        
# recent can't have real tests as it depends on a recent play

class TestRecent(unittest.TestCase):
    def test_if_fail(self):
        return # api key not working
        try:
            r = asyncio.run(recent.recent({}, ["!recent", "WhiteCat"]))
        except Exception as e:
            try:
                r = asyncio.run(recent.recent({}, ["!recent", "Vaxei"]))
            except Exception as e:
                try:
                    r = asyncio.run(recent.recent({}, ["!recent", "BTMC"]))
                except Exception as e:
                    self.fail(e)

# top play test will be made later (maybe I will use peppys)

class TestTop(unittest.TestCase):
    def test_if_fail(self):
        return # api key not working
        try:
            r = asyncio.run(top.top({}, ["!top", "1", "WhiteCat"]))
        except Exception as e:
            self.fail(e)
            
# user can't have real tests as it depends on a pp (unless they are offline forever)

class TestUser(unittest.TestCase):
    def test_if_fail(self):
        return # api key not working
        try:
            r = asyncio.run(user.user({}, ["!user", "peppy"]))
        except Exception as e:
            self.fail(e)

if __name__ == '__main__':
    try:
        unittest.main()
    except RuntimeError:
        pass