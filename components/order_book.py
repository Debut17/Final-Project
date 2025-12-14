import threading
import requests
from tkinter import ttk

BINANCE_REST = "https://api.binance.com"


class OrderBook(ttk.Frame):
    def __init__(self, parent, symbol):
        super().__init__(parent, padding=8)
        self.symbol = symbol

        ttk.Label(self, text="Order Book (Top 10)", font=("Arial", 11, "bold")).pack()

        self.tree = ttk.Treeview(
            self,
            columns=("bid_p", "bid_q", "ask_p", "ask_q"),
            show="headings",
            height=10
        )
        self.tree.heading("bid_p", text="Bid Price")
        self.tree.heading("bid_q", text="Bid Qty")
        self.tree.heading("ask_p", text="Ask Price")
        self.tree.heading("ask_q", text="Ask Qty")

        for c in self.tree["columns"]:
            self.tree.column(c, anchor="center", width=90)

        self.tree.pack(fill="both", expand=True)

        self.update_data()

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.update_data()

    def update_data(self):
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            r = requests.get(
                f"{BINANCE_REST}/api/v3/depth",
                params={"symbol": self.symbol, "limit": 10},
                timeout=6
            )
            r.raise_for_status()
            data = r.json()
            self.after(0, self._update_table, data)
        except Exception:
            pass

    def _update_table(self, data):
        self.tree.delete(*self.tree.get_children())

        bids = data.get("bids", [])
        asks = data.get("asks", [])

        for i in range(10):
            bp, bq = bids[i] if i < len(bids) else ("", "")
            ap, aq = asks[i] if i < len(asks) else ("", "")
            self.tree.insert("", "end", values=(bp, bq, ap, aq))
