def what_can_buy(account: int, movie: int, pie: int) -> str:
    if account >= movie + pie:
        return "все купишь"
    elif account >= movie and account >= pie:
        return "только одно"
    elif account >= movie:
        return "только кино"
    elif account >= pie:
        return "только пирожок"
    else:
        return "ничего не купишь"


if __name__ == "__main__":
    print("task5")
    account = int(input())
    movie = int(input())
    pie = int(input())
    print(what_can_buy(account, movie, pie))
