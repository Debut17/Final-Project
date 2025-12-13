import requests
from config import BINANCE_REST

class BinanceREST:
    @staticmethod
    def ticker_24hrs(symbol, timeout=8):
        url = f"{BINANCE_REST}/api/v3/ticker/24hr"
        r = requests.get(url, params={"symbol": symbol}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    
    @staticmethod
    def klines(symbol, interval="1m", limit=120, timeout=8):
        url = f"{BINANCE_REST}/api/v3/klines"
        r = requests.get(
            url,
            params={"symbol": symbol, "interval": interval, "limit": limit},
            timeout=timeout
        )
        r.raise_for_status()
        return r.json()
    