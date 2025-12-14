# Crypto Dashboard (Tkinter)

A desktop cryptocurrency dashboard built with **Python** and **Tkinter**.  
This application allows users to track real-time crypto prices, toggle selected coins, and visualize data in an interactive and user-friendly interface.

---

## Features

- Real-time cryptocurrency price display
- Color-coded price changes (green for increase, red for decrease)
- 24-hour price change & percentage
- 24-hour trading volume display
- Toggle buttons to show / hide selected coins (e.g. BTC, ETH)
- Interactive UI with active/inactive button states
- Desktop application using Tkinter
- Modular and readable Python code structure
- Candlestick price chart (Matplotlib)

---

## Technologies Used

- **Python 3.10+**
- **Tkinter** (GUI framework)
- **Matplotlib** (Candlestick charts)
- **Requests** (API calls)
- **WebSocket-client** (Real-time data streaming)
- **Public Crypto API** (e.g. Binance / CoinGecko)

---

## Project Structure
```
crypto_dashboard/
│
├── main.py                 # Entry point (only starts the app)
│
├── components/
│   ├── __init__.py
│   ├── ticker_card.py      # TickerCard class
│   ├── candle_chart.py     # CandleChart class
│   ├── order_book.py       # Order book (top 10 bids/asks)
│   └── recent_trades.py    # Recent trades panel
│
├── services/
│   ├── __init__.py
│   ├── binance_rest.py     # BinanceREST class
│   └── ticker_stream.py    # TickerStream (WebSocket)
│
├── config.py               # SymbolConfig, constants
├── dashboard_prefs.json    # Auto-saved user preferences           
├── README.md               # Project documentation
└── requirements.txt
```
---

## How to Run

1. **Clone the repository**
    ```bash
    git clone https://github.com/Debut17/Final-Project
    cd Final-Project
    ```
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the application**
    ```bash
    python main.py
    ```
---

## Example Coins Supported
- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum)
- SOLUSDT (Solana)
- BNBUSDT (Binance Coin)
- XRPUSDT (XRP)
---

## Design Notes
- Button state changes visually when active/inactive
- Dashboard updates without restarting the app
- Code follows basic Object-Oriented Programming (OOP)
- Thread-safe UI updates using Tk.after()
---
