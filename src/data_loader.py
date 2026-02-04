import yfinance as yf
import pandas as pd
import os

class DataLoader:
    # 1. Inicjalizacja klasy i przygotowanie folderu na dane
    def __init__(self, storage_path='data'):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    # 2. Główna logika zarządzania danymi (pobieranie lub wczytywanie z cache)
    # ZMIANA: Dodano parametr force_update, aby móc wymusić pobranie świeżych danych
    def get_data(self, ticker: str, period: str = "20y", force_update: bool = False):
        file_path = os.path.join(self.storage_path, f"{ticker}_d1.csv")
        
        # 3. Sprawdzenie czy dane istnieją lokalnie przed pobieraniem
        # ZMIANA: Sprawdzamy też, czy nie wymuszono aktualizacji
        if not force_update and os.path.exists(file_path):
            print(f"Wczytywanie {ticker} z dysku...")
            return pd.read_csv(file_path, index_col=0, parse_dates=True)
        
        # 4. Pobieranie danych z zewnętrznego źródła (Yahoo Finance)
        print(f"Pobieranie {ticker} z sieci (odświeżanie)...")
        df = yf.download(ticker, period=period, interval="1d")
        
        if df.empty:
            return None
            
        # 5. Standaryzacja formatu danych (czyszczenie nagłówków)
        # ZMIANA: Dodano jawne sprawdzenie 'df is not None', aby uciszyć błędy Pylance
        if df is not None:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            # 6. Zapisanie pobranych danych do pliku CSV
            df.to_csv(file_path)
            
        return df

# 7. Blok uruchomieniowy (testowy)
if __name__ == "__main__":
    loader = DataLoader()
    
    # Przykład użycia: wymuszamy pobranie najnowszych danych
    df_spy = loader.get_data("SPY", force_update=True)
    
    if df_spy is not None:
        # Wyświetlamy kształt danych (ile wierszy i kolumn)
        print(f"\nStruktura danych (wiersze, kolumny): {df_spy.shape}")
        
        # Wyświetlamy początek danych
        print("\n--- OTO TWOJE DANE (POCZĄTEK) ---")
        print(df_spy.head().to_string())
        
        # Wyświetlamy koniec danych - JEDNORAZOWO
        print("\n--- OTO TWOJE DANE (KONIEC) ---")
        print(df_spy.tail().to_string())
        
        # Podsumowanie liczby dni
        print(f"\nCałkowita liczba dni giełdowych: {len(df_spy)}")