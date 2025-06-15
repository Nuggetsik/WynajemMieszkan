# Główny moduł do uruchamiania systemu zarządzania wynajmem
from models import App

# Globalna zmienna dla nazwy pliku danych
DATA_FILE = "data.json"

def main():
    """Inicjalizacja i uruchomienie aplikacji."""
    app = App(DATA_FILE)
    app.run()

if __name__ == "__main__":
    main()