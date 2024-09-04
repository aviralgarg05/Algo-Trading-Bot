import tkinter as tk
from tkinter import ttk
import yfinance as yf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_data(symbol, period="1mo", interval="1d"):
    stock_data = yf.download(symbol, period=period, interval=interval)
    return stock_data

def plot_candlestick(data, ax):
    candlesticks = zip(data.index, data['Open'], data['Close'], data['High'], data['Low'])
    for i, (date, open, close, high, low) in enumerate(candlesticks):
        color = 'green' if close >= open else 'red'
        ax.plot([i, i], [low, high], color='black')
        ax.plot([i - 0.3, i + 0.3], [open, open], color=color, linewidth=6)
        ax.plot([i - 0.3, i + 0.3], [close, close], color=color, linewidth=6)
    ax.set_title('Candlestick Chart')

def plot_line(data, ax):
    ax.plot(data.index, data['Close'], label="Close Price")
    ax.set_title('Line Chart')

def plot_ohlc(data, ax):
    ohlc = zip(data.index, data['Open'], data['High'], data['Low'], data['Close'])
    for i, (date, open, high, low, close) in enumerate(ohlc):
        color = 'green' if close >= open else 'red'
        ax.plot([i, i], [low, high], color='black')
        ax.plot([i, i], [open, close], color=color, linewidth=4)
    ax.set_title('OHLC Chart')

def update_chart():
    symbol = entry_symbol.get()
    period = period_var.get()
    interval = interval_var.get()
    chart_type = chart_type_var.get()
    data = fetch_data(symbol, period, interval)
    
    for widget in frame_chart.winfo_children():
        widget.destroy()
    
    if not data.empty:
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        if chart_type == "Candlestick":
            plot_candlestick(data, ax)
        elif chart_type == "Line":
            plot_line(data, ax)
        elif chart_type == "OHLC":
            plot_ohlc(data, ax)

        ax.set_xticks(range(len(data.index)))
        ax.set_xticklabels(data.index.strftime('%Y-%m-%d'), rotation=45, ha='right')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame_chart)
        canvas.get_tk_widget().pack()
        canvas.draw()
    else:
        label_status.config(text="No data found. Check the symbol and try again.")

root = tk.Tk()
root.title("Stock and Crypto Analytics")

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

example_symbols = ["AAPL", "GOOGL", "AMZN", "TSLA", "BTC-USD", "ETH-USD", "DOGE-USD"]

frame_top = ttk.Frame(scrollable_frame)
frame_top.pack(pady=10)

ttk.Label(frame_top, text="Symbol:").pack(side=tk.LEFT, padx=5)
entry_symbol = ttk.Combobox(frame_top, values=example_symbols, width=20)
entry_symbol.set("AAPL")
entry_symbol.pack(side=tk.LEFT, padx=5)

ttk.Label(frame_top, text="Period:").pack(side=tk.LEFT, padx=5)
period_var = tk.StringVar(value="1mo")
ttk.Combobox(frame_top, textvariable=period_var, values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]).pack(side=tk.LEFT, padx=5)

ttk.Label(frame_top, text="Interval:").pack(side=tk.LEFT, padx=5)
interval_var = tk.StringVar(value="1d")
ttk.Combobox(frame_top, textvariable=interval_var, values=["1m", "2m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"]).pack(side=tk.LEFT, padx=5)

ttk.Label(frame_top, text="Chart Type:").pack(side=tk.LEFT, padx=5)
chart_type_var = tk.StringVar(value="Candlestick")
ttk.Combobox(frame_top, textvariable=chart_type_var, values=["Candlestick", "Line", "OHLC"]).pack(side=tk.LEFT, padx=5)

ttk.Button(frame_top, text="Fetch", command=update_chart).pack(side=tk.LEFT, padx=5)

frame_chart = ttk.Frame(scrollable_frame)
frame_chart.pack(pady=10)

label_status = ttk.Label(scrollable_frame, text="")
label_status.pack(pady=5)

frame_bottom = ttk.Frame(scrollable_frame)
frame_bottom.pack(pady=10)

ttk.Button(frame_bottom, text="Buy").pack(side=tk.LEFT, padx=10)
ttk.Button(frame_bottom, text="Sell").pack(side=tk.LEFT, padx=10)

canvas.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.pack(side=tk.RIGHT, fill="y")

root.mainloop()
