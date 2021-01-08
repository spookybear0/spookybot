import unittest, asyncio
from commands import rank

class TestRank(unittest.TestCase):

    def test_manual_type_pp(self):
        r = asyncio.run(rank({}, ["!rank", "100", "pp"], True))
        self.assertAlmostEqual(2023918, r, 10)
        
    def test_manual_type_pp2(self):
        r = asyncio.run(rank({}, ["!rank", "200pp", "pp"], True))
        self.assertAlmostEqual(1503935, r, 10)
        
    def test_manual_type_pp_str(self):
        r = asyncio.run(rank({}, ["!rank", "1k", "pp"], True))
        self.assertAlmostEqual(573709, r, 10)
        
    def test_manual_type_pp_str2(self):
        r = asyncio.run(rank({}, ["!rank", "1kpp", "pp"], True))
        self.assertAlmostEqual(573709, r, 10)
    
    def test_manual_type_rank(self):
        r = asyncio.run(rank({}, ["!rank", "300k", "rank"], True))
        self.assertAlmostEqual(1971, r, 10)
        
    def test_manual_type_rank2(self):
        r = asyncio.run(rank({}, ["!rank", "300000", "rank"], True))
        self.assertAlmostEqual(1971, r, 10)
        
    def test_rank_str(self):
        r = asyncio.run(rank({}, ["!rank", "1k"], True))
        self.assertAlmostEqual(10492, r, 10)
        
    def test_rank_pp_str(self):
        r = asyncio.run(rank({}, ["!rank", "1kpp"], True))
        self.assertAlmostEqual(573709, r, 10)

if __name__ == '__main__':
    unittest.main()