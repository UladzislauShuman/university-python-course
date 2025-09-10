import pytest
from lab1.src.task5 import what_can_buy

def test_buy_both():
    assert what_can_buy(10, 5, 2) == "все купишь"

def test_buy_only_one():
    assert what_can_buy(10, 5, 7) == "только одно"

def test_only_movie():
    assert what_can_buy(3, 2, 5) == "только кино"

def test_only_pie():
    assert what_can_buy(3, 5, 2) == "только пирожок"

def test_buy_nothing():
    assert what_can_buy(10, 50, 20) == "ничего не купишь"
    
    
# same but in another syntaxis
test_data = [
    (10, 5, 2,   "все купишь"),
    (10, 5, 7,   "только одно"),
    (3,  2, 5,   "только кино"),
    (3,  5, 2,   "только пирожок"),
    (10, 50, 20, "ничего не купишь")
]

@pytest.mark.parametrize("money, movie_price, pie_price, expected", test_data)
def test_what_can_buy_scenarios(money, movie_price, pie_price, expected):
    assert what_can_buy(money, movie_price, pie_price) == expected