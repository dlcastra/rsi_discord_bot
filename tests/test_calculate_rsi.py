from bot.find_rsi import calculate_rsi
from .special_variables import kline_list


def test_calculate_rsi():
    rsi_result = calculate_rsi(kline_list)  # RSI for this kline list will 31.82476920462436

    assert rsi_result != 0
    assert rsi_result is not None
    assert rsi_result == 31.82476920462436


def test_klines_empty_list():
    kline_list = []
    rsi_result = calculate_rsi(kline_list) # Return None if kline list is empty

    assert rsi_result is None
    assert type(rsi_result) is not int
