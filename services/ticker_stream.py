import json
import threading
import time
import websocket
from config import BINANCE_WS_BASE

class TickerStream:
    def __init__(self, symbol, on_tick, on_status=lambda msg: None):
        self.symbol = symbol.lower()
        self.on_tick = on_tick
        self.on_status = on_status
        
        self.ws = None
        self.active = False
        
    def start(self):
        if self.active:
            return
        self.active = True
        
        url = f"{BINANCE_WS_BASE}/{self.symbol}@ticker"
        
        def on_message(ws, msg):
            if not self.active:
                return
            try:
                data = json.loads(msg)
                self.on_tick(
                    float(data["c"]),
                    float(data["p"]),
                    float(data["P"]),
                    float(data["v"])
                )
            except Exception as e:
                self.on_status(f"{self.symbol.upper()} parse error: {e}")
            
        def on_error(ws, err):
            self.on_status(f"{self.symbol.upper()} WS error: {err}")
        
        def on_open(ws):
            self.on_status(f"{self.symbol.upper()} WS connected")
            
        def on_close(ws, status_code, msg):
            self.on_status(f"{self.symbol.upper()} WS closed")
            
        self.ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_error=on_error,
            on_open=on_open,
            on_close=on_close
        )
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def stop(self):
        self.active = False
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None