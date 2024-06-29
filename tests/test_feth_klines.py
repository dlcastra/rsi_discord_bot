from pybit.unified_trading import HTTP

from bot.find_rsi import fetch_klines


def test_fetch_klines():
    session = HTTP(testnet=True)
    category = "spot"
    symbol = "SOLUSDT"
    interval = 60
    limit = 1

    response = fetch_klines(session, category, symbol, interval, limit)

    # NEGATIVE CASES
    assert response is not None
    assert len(response) != 0
    assert response != [["1670608800000", "13.64", "13.64", "13.565", "13.625", "8882", "120850.4695"]]

    # POSITIVE CASES
    assert type(response) is list
    assert response == [["1719655200000", "26", "26", "26", "26", "0", "0"]]
