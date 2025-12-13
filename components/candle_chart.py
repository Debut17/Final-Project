import tkinter as tk
from tkinter import ttk
from collections import deque

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from services.binance_rest import BinanceREST

class CandleChart(ttk.Frame):
    def __init__(self, parent, interval="1m", limit=120):
        super().__init__(parent, padding=12)
        
        self.symbol = None
        self.interval = interval
        self.limit = limit
        
        self.active = False
        self.after_id = None
        
        self.data = deque(maxlen=self.limit)
        
        self.figure = Figure(figsize=(8,4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("CandleStick Chart")
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def set_symbol(self, symbol: str):
        self.symbol = symbol
        self.ax.set_title(f"{symbol} CandleStick ({self.interval})")
        self.refresh()
        
    def start(self, root: tk.Tk):
        self.active = True
        self._schedule(root)
        
    def stop(self, root: tk.Tk):
        self.active = False
        if self.after_id is not None:
            root.after_cancel(self.after_id)
            self.after_id = None
            
    def _schedule(self, root: tk.Tk):
        if not self.active:
            return
        
        self.refresh()
        self.after_id = root.after(10_00, lambda: self._schedule(root))
        
    def refresh(self):
        if not self.symbol:
            return
        
        try:
            klines = BinanceREST.klines(self.symbol, interval=self.interval, limit=self.limit)
            
            self.data.clear()
            for k in klines:
                o = float(k[1])
                h = float(k[2])
                l = float(k[3])
                c = float(k[4])
                self.data.append((o, h, l, c))
                
            self._draw()
            
        except Exception as e:
            self._draw_error(e)
            
    def _draw(self):
        self.ax.clear()
        self.ax.set_title(f"{self.symbol} CandleStick ({self.interval})")
        self.ax.set_xlabel("Candles")
        self.ax.set_ylabel("Price")
        
        for i, (o, h, l , c) in enumerate(self.data):
            color = "green" if c >= o else "red"
            
            self.ax.plot([i,i], [l,h], color=color, linewidth=1)
            
            bottom = min(o, c)
            height = abs(c - o)
            if height == 0:
                height = 0.0001
                
            self.ax.bar(
                i,
                height,
                bottom=bottom,
                width=0.6,
                color=color,
                align="center"
            )
            
        self.canvas.draw_idle()
        
    def _draw_error(self, error):
        self.ax.clear()
        self.ax.set_title("Chart Error")
        self.ax.text(
            0.5, 0.5,
            str(error),
            ha="center",
            va="center",
            transform=self.ax.transAxes
        )
        self.canvas.draw_idle()
        