import vectorbt as vbt
from data_loader import DataLoader 
from typing import Any
import numpy as np
import itertools

def run_backtest():
    # --- MODUŁ 1: Inicjalizacja i pobieranie danych ---
    loader = DataLoader() 
    df: Any = loader.get_data("SPY", force_update=True) 
  
    if df is None:
        print("Błąd: Nie udało się pobrać danych.")
        return

    close = df['Close']

    # --- MODUŁ 2: Definicja zakresów optymalizacji ---
    fast_windows = np.arange(10, 51, 5)   
    slow_windows = np.arange(100, 251, 10) 

# --- MODUŁ 3: Masowe obliczenia (Wersja odporna na Pylance) ---
    # Ręcznie tworzymy listę par: [(10, 100), (10, 110), ..., (50, 250)]
    param_grid = list(itertools.product(fast_windows, slow_windows))
    
    # Rozdzielamy pary na dwie osobne listy dla vbt
    fast_params = [p[0] for p in param_grid]
    slow_params = [p[1] for p in param_grid]

    # Uruchamiamy obliczenia - podajemy listy o tej samej długości (144)
    # Używamy Any, aby Pylance przestał podkreślać wynik
    fast_ma: Any = vbt.MA.run(close, window=fast_params)
    slow_ma: Any = vbt.MA.run(close, window=slow_params)

    # Obliczamy sygnały
    entries = fast_ma.ma_crossed_above(slow_ma) # type: ignore
    exits = fast_ma.ma_crossed_below(slow_ma) # type: ignore

    # --- MODUŁ 4: Symulacja portfela ---
    pf = vbt.Portfolio.from_signals(
        close, entries, exits, 
        init_cash=10000, 
        fees=0.001, 
        freq='D'
    )

    # --- MODUŁ 5: Wyciąganie najlepszych wyników ---
    returns = pf.total_return()
    
    best_return = returns.max()
    best_params = returns.idxmax()

    print("\n--- OPTYMALIZACJA ZAKOŃCZONA ---")
    print(f"Liczba przetestowanych kombinacji: {len(returns)}")
    print(f"Najlepszy zwrot: {best_return * 100:.2f}%")
    print(f"Najlepsze parametry (szybka, wolna): {best_params}")

    # --- MODUŁ 6: Statystyki dla najlepszej strategii ---
    best_pf = pf[best_params]
    print(f"\n--- SZCZEGÓŁOWE STATYSTYKI NAJLEPSZEJ KOMBINACJI ---")
    print(best_pf.stats())

if __name__ == "__main__":
    run_backtest()