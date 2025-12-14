import threading
import requests
import tkinter as tk
from tkinter import ttk

BINANCE_REST = "https://api.binance.com"


class RecentTrades(ttk.Frame):
    def __init__(self, parent, symbol):
        super().__init__(parent, padding=8)
        self.symbol = symbol

        ttk.Label(self, text="Recent Trades (Last 10)", font=("Arial", 11, "bold")).pack()

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.pack(fill="both", expand=True)

        self.update_data()

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.update_data()

    def update_data(self):
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            r = requests.get(
                f"{BINANCE_REST}/api/v3/trades",
                params={"symbol": self.symbol, "limit": 10},
                timeout=6
            )
            r.raise_for_status()
            trades = r.json()
            self.after(0, self._update_list, trades)
        except Exception:
            pass

    def _update_list(self, trades):
        self.listbox.delete(0, tk.END)
        for t in trades:
            price = float(t["price"])
            qty = float(t["qty"])
            side = "BUY" if not t["isBuyerMaker"] else "SELL"
            self.listbox.insert(tk.END, f"{side:<4} {qty:.5f} @ {price:.2f}")
