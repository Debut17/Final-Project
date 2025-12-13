from dataclasses import dataclass

BINANCE_REST = "https://api.binance.com"
BINANCE_WS_BASE = "wss://stream.binance.com:9443/ws"

@dataclass
class SymbolConfig:
    symbol: str
    title: str
    logo_text: str
    