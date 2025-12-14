import tkinter as tk
from tkinter import ttk

from config import SymbolConfig
from components.ticker_card import TickerCard
from components.candle_chart import CandleChart

from components.order_book import OrderBook
from components.recent_trades import RecentTrades

import json

BTN_BG = "#eaeaea"
BTN_HOVER = "#d6d6d6"
BTN_ACTIVE = "#bfbfbf"
PREF_FILE = "dashboard_prefs.json"

class CryptoDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Dashboard")
        self.geometry("1100x650")
        
        self.symbols = [
            SymbolConfig("BTCUSDT", "BTC/USDT", "₿"),
            SymbolConfig("ETHUSDT", "ETH/USDT", "Ξ"),
            SymbolConfig("SOLUSDT", "SOL/USDT", "◎"),
            SymbolConfig("BNBUSDT", "BNB/USDT", "🟡"),
            SymbolConfig("XRPUSDT", "XRP/USDT", "✕"),
        ]
        
        self.cards = {}
        self.visible = {}
        self.active_symbol = "BTCUSDT"
        self.chart_visible = True
        
        try:
            with open(PREF_FILE, "r") as f:
                prefs = json.load(f)
            self.active_symbol = prefs.get("active_symbol", self.active_symbol)
            self.chart_visible = prefs.get("chart_visible", self.chart_visible)

            saved_visible = prefs.get("visible", {})
            for cfg in self.symbols:
                self.visible[cfg.symbol] = bool(saved_visible.get(cfg.symbol, True))
        except Exception:
            for cfg in self.symbols:
                self.visible[cfg.symbol] = True
        
        self.control_frame = ttk.Frame(self, padding=10)
        self.control_frame.pack(fill="x")

        self.ticker_frame = ttk.Frame(self, padding=10)
        self.ticker_frame.pack(fill="x")

        self.chart_frame = ttk.Frame(self, padding=10)
        self.chart_frame.pack(fill="both", expand=True)
        
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(fill="both", expand=True)

        self.order_book = OrderBook(self.bottom_frame, self.active_symbol)
        self.order_book.pack(side="left", fill="both", expand=True)

        self.trades = RecentTrades(self.bottom_frame, self.active_symbol)
        self.trades.pack(side="left", fill="both", expand=True)
        
        self.toggle_btns = {}

        for cfg in self.symbols:
            btn_frame = tk.Frame(
                self.control_frame,
                bg=BTN_BG,
                bd=1,
                relief="solid",
                cursor="hand2"
            )
            
            btn_label = tk.Label(
                btn_frame,
                text=f"{cfg.logo_text}  {cfg.title.split('/')[0]}",
                bg=BTN_BG,
                font=("Arial", 10, "bold")
            )
            
            btn_label.pack(padx=14, pady=6)
            btn_frame.pack(side="left", padx=8)
            
            btn_frame.bind("<Enter>", lambda e, b=btn_frame, l=btn_label: self._hover_on(b, l))
            btn_frame.bind("<Leave>", lambda e, b=btn_frame, l=btn_label: self._hover_off(b, l))
            btn_frame.bind("<Button-1>", lambda e, s=cfg.symbol: self.toggle_ticker(s))

            btn_label.bind("<Enter>", lambda e, b=btn_frame, l=btn_label: self._hover_on(b, l))
            btn_label.bind("<Leave>", lambda e, b=btn_frame, l=btn_label: self._hover_off(b, l))
            btn_label.bind("<Button-1>", lambda e, s=cfg.symbol: self.toggle_ticker(s))

            self.toggle_btns[cfg.symbol] = (btn_frame, btn_label)
            
        self.chart_btn = ttk.Button(
            self.control_frame,
            text="Hide Chart",
            command=self.toggle_chart
        )
        self.chart_btn.pack(side="right", padx=8)
        
        self.status_var = tk.StringVar(value="")
        ttk.Label(self.control_frame, textvariable=self.status_var).pack(side="right", padx=8)
        
        for cfg in self.symbols:
            card = TickerCard(self.ticker_frame, cfg, self.select_symbol)

            if self.visible.get(cfg.symbol, True):
                card.pack(side="left", padx=10, fill="x", expand=True)
                card.start(self, self.set_status)
            else:
                card.pack_forget()

                frame, label = self.toggle_btns[cfg.symbol]
                coin = cfg.symbol.replace("USDT", "")
                label.config(text=f"{cfg.logo_text}  Show {coin}")

            self.cards[cfg.symbol] = card
        
        self.chart = CandleChart(self.chart_frame)
        self.chart.pack(fill="both", expand=True)
        self.chart.set_symbol(self.active_symbol)
        self.chart.start(self)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def set_status(self, msg: str):
        print(msg)
        self.status_var.set(msg)
    
    def select_symbol(self, symbol: str):
        self.active_symbol = symbol
        self.set_status(f"Selected: {symbol}")
        
        self.order_book.set_symbol(symbol)
        self.trades.set_symbol(symbol)

        for sym, card in self.cards.items():
            card.set_selected(sym == symbol)

        if self.chart_visible:
            self.chart.set_symbol(symbol)

    def toggle_ticker(self, symbol: str):
        card = self.cards[symbol]
        frame, label = self.toggle_btns[symbol]
        
        coin = symbol.replace("USDT", "")
        icon = next(cfg.logo_text for cfg in self.symbols if cfg.symbol == symbol)

        if self.visible[symbol]:
            card.stop()
            card.pack_forget()
            self.visible[symbol] = False

            label.config(text=f"{icon}  Show {coin}")
            self.set_status(f"{symbol} hidden")
        else:
            card.pack(side="left", padx=10, fill="x", expand=True)
            card.start(self, self.set_status)
            self.visible[symbol] = True

            label.config(text=f"{icon}  Hide {coin}")
            self.set_status(f"{symbol} shown")
            
    def toggle_chart(self):
        if self.chart_visible:
            self.chart.stop(self)
            self.chart.pack_forget()
            self.chart_visible = False
            self.chart_btn.config(text="Show Chart")
            self.set_status("Chart hidden")
        else:
            self.chart.pack(fill="both", expand=True)
            self.chart.set_symbol(self.active_symbol)
            self.chart.start(self)
            self.chart_visible = True
            self.chart_btn.config(text="Hide Chart")
            self.set_status("Chart shown")
        
    def on_close(self):
        for card in self.cards.values():
            card.stop()
        try:
            prefs = {
                "active_symbol": self.active_symbol,
                "chart_visible": self.chart_visible,
                "visible": self.visible
            }
            with open(PREF_FILE, "w") as f:
                json.dump(prefs, f, indent=2)
        except Exception:
            pass
        
        try:
            self.chart.stop(self)
        except Exception:
            pass
        
        self.destroy()
        
    def _hover_on(self, frame, label):
        frame.config(bg=BTN_HOVER)
        label.config(bg=BTN_HOVER)

    def _hover_off(self, frame, label):
        frame.config(bg=BTN_BG)
        label.config(bg=BTN_BG)

if __name__ == "__main__":
    app = CryptoDashboard()
    app.mainloop()
    