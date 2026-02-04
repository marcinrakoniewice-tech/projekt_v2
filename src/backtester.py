import vectorbt as vbt
from data_loader import DataLoader # To zostaje
from typing import Any

def run_backtest():
    # 1. Musisz najpierw stworzyć obiekt loader
    loader = DataLoader() 
    
    # 2. Teraz wywołujesz na nim metodę get_data
    df: Any = loader.get_data("SPY", force_update=True) 
  
    if df is None:
        print("Błąd: Nie udało się pobrać danych.")
        return

    close = df['Close']

    # 2. Obliczenia strategii
    fast_ma = vbt.MA.run(close, 50)
    slow_ma = vbt.MA.run(close, 200)

    entries = fast_ma.ma_crossed_above(slow_ma) # type: ignore
    exits = fast_ma.ma_crossed_below(slow_ma) # type: ignore

    # 3. Symulacja (dodano freq='D', aby pozbyć się ostrzeżeń)
    pf = vbt.Portfolio.from_signals(
        close, entries, exits, 
        init_cash=10000, 
        fees=0.001, 
        freq='D'
    )
    
    print("\n--- WYNIKI STRATEGII SMA 50/200 ---")
    print(pf.stats())

if __name__ == "__main__":
    run_backtest()