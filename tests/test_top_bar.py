from datetime import datetime

from ui.top_bar import TopBar


def test_market_state_resolves_pre_open_open_and_closed():
    bar = TopBar()

    assert bar._market_state(datetime(2024, 1, 2, 9, 10)) == "PRE OPEN"
    assert bar._market_state(datetime(2024, 1, 2, 9, 15)) == "OPEN"
    assert bar._market_state(datetime(2024, 1, 2, 15, 31)) == "CLOSED"
    assert bar._market_state(datetime(2024, 1, 6, 9, 15)) == "CLOSED"
