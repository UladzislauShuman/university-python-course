import unittest
from lab1.src.task5 import what_can_buy

class TestClass5(unittest.TestCase):
    def test_buy_both(self):
        self.assertEqual(what_can_buy(10,5,2), "все купишь")
    def test_buy_only_one(self):
        self.assertEqual(what_can_buy(10, 5, 7), "только одно")

    def test_only_movie(self):
        self.assertEqual(what_can_buy(3, 2, 5), "только кино")

    def test_only_pie(self):
        self.assertEqual(what_can_buy(3, 5, 2), "только пирожок")

    def test_buy_nothing(self):
        self.assertEqual(what_can_buy(10, 50, 20), "ничего не купишь")
        
if __name__ == "__main__":
    unittest.main()