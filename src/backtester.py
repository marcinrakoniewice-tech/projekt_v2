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

    # --- MODUŁ 3: Masowe obliczenia ---
    param_grid = list(itertools.product(fast_windows, slow_windows))
    fast_params = [p[0] for p in param_grid]
    slow_params = [p[1] for p in param_grid]

    fast_ma: Any = vbt.MA.run(close, window=fast_params)
    slow_ma: Any = vbt.MA.run(close, window=slow_params)

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
    best_params = returns.idxmax()

    print("\n--- OPTYMALIZACJA ZAKOŃCZONA ---")
    print(f"Liczba przetestowanych kombinacji: {len(returns)}")
    print(f"Najlepszy zwrot: {returns.max() * 100:.2f}%")
    print(f"Najlepsze parametry (szybka, wolna): {best_params}")

    # --- MODUŁ 6: Statystyki dla najlepszej strategii ---
    best_pf = pf[best_params]
    print(f"\n--- SZCZEGÓŁOWE STATYSTYKI NAJLEPSZEJ KOMBINACJI ---")
    print(best_pf.stats())

    # --- MODUŁ 7: Ulepszony Wykres (Musi mieć wcięcie!) ---
    print("\nGenerowanie wykresu najlepszej strategii...")
    
    # Szerokość i wysokość dostosowana do Twojego ekranu
    fig = best_pf.plot(width=1600, height=1000)
    fig.update_layout(autosize=True)

    output_path = "best_strategy_chart.html"
    fig.write_html(output_path)

    print(f"Sukces! Wykres zapisany jako: {output_path}")

if __name__ == "__main__":
    run_backtest()