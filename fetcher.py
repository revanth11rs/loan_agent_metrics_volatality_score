# fetcher.py
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def fetch_historical_prices(id: str, days: int) -> list[float]:
    """
    Returns the list of daily closing prices over the past `days` days.
    """
    data = cg.get_coin_market_chart_by_id(
        id=id,
        vs_currency="usd",
        days=days,
        interval="daily"
    )["prices"]   # [[timestamp, price], …]
    return [p[1] for p in data]

def fetch_pct_change(id: str, days: int) -> float:
    """
    % change over the last `days` days.
    """
    prices = fetch_historical_prices(id, days)
    start, end = prices[0], prices[-1]
    return (end - start) / start * 100.0