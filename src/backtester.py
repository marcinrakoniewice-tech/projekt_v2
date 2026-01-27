# 1. Import niezbędnych bibliotek
import vectorbt as vbt
from data_loader import DataLoader

# 2. Logika obliczeniowa strategii
def run_backtest():
    loader = DataLoader()
    df = loader.get_data("SPY") # Wczyta z dysku
    
    close = df['Close']

    # Obliczamy średnie kroczące (SMA 50 i 200)
    fast_ma = vbt.MA.run(close, 50)
    slow_ma = vbt.MA.run(close, 200)

    # Definiujemy sygnały wejścia i wyjścia
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    # Symulacja portfela
    pf = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000, fees=0.001)
    
    print("\n--- WYNIKI STRATEGII SMA 50/200 ---")
    print(pf.stats())

# 3. Start skryptu
if __name__ == "__main__":
    run_backtest()