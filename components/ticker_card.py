import tkinter as tk
from tkinter import ttk
from services.ticker_stream import TickerStream

CARD_BG = "#eeeeee"
CARD_HOVER = "#d9d9d9"
CARD_ACTIVE = "#c9c9c9"

class TickerCard(ttk.Frame):
    def __init__(self, parent, cfg, on_select):
        super().__init__(parent)
        self.cfg = cfg
        self.on_select = on_select
        
        self.stream = None
        self.active = False
        self.selected = False
        
        self.price_var = tk.StringVar(value="--")
        self.change_var = tk.StringVar(value="--")
        
        self.card = tk.Frame(
            self,
            bg=CARD_BG,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#b0b0b0",
            cursor="hand2"
        )
        self.card.pack(fill="both", expand=True, padx=6, pady=6)
        
        self.title_lbl = tk.Label(self.card, text=cfg.title, bg=CARD_BG, font=("Arial", 11, "bold"))
        self.title_lbl.pack(pady=(10, 2))

        self.price_lbl = tk.Label(self.card, textvariable=self.price_var, bg=CARD_BG, font=("Arial", 16, "bold"))
        self.price_lbl.pack(pady=(0, 2))

        self.change_lbl = tk.Label(self.card, textvariable=self.change_var, bg=CARD_BG, font=("Arial", 10))
        self.change_lbl.pack(pady=(0, 10))
        
        widgets = (self.card, self.title_lbl, self.price_lbl, self.change_lbl)
        for w in widgets:
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Button-1>", self._clicked)
            
    def _set_bg(self, color: str):
        self.card.config(bg=color)
        self.title_lbl.config(bg=color)
        self.price_lbl.config(bg=color)
        self.change_lbl.config(bg=color)
        
    def _on_enter(self, _evt=None):
        self._set_bg(CARD_HOVER)

    def _on_leave(self, _evt=None):
        self._set_bg(CARD_ACTIVE if self.selected else CARD_BG)
        
    def set_selected(self, selected: bool):
        self.selected = selected
        self._set_bg(CARD_ACTIVE if self.selected else CARD_BG)

    def _clicked(self, _evt=None):
        self.on_select(self.cfg.symbol)
        
    def start(self, root: tk.Tk, status_cb):
        if self.active:
            return
        self.active = True
        
        def on_tick(price, change, percent, volume):
            root.after(0, self.update_display, price, change, percent)
            
        self.stream = TickerStream(self.cfg.symbol, on_tick, status_cb)
        self.stream.start()
        
        if status_cb:
            status_cb(f"{self.cfg.symbol} stream started")

    def stop(self):
        self.active = False
        if self.stream:
            self.stream.stop()
            self.stream = None
            
    def update_display(self, price, change, percent):
        if not self.active:
            return
        sign = "+" if change >= 0 else ""
        self.price_var.set(f"{price:,.2f}")
        self.change_var.set(f"{sign}{change:,.2f} ({sign}{percent:.2f}%)")

        if change >= 0:
            self.price_lbl.config(fg="green")
            self.change_lbl.config(fg="green")
        else:
            self.price_lbl.config(fg="red")
            self.change_lbl.config(fg="red")