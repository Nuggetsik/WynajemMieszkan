# Funkcje pomocnicze do pracy z plikami
import json

def load_data(filename="data.json"):
    """Ładowanie danych z pliku JSON."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje, tworzenie nowego.")
        return {}
    except json.JSONDecodeError:
        print("Błąd wczytywania danych JSON.")
        return {}
    finally:
        print("Zakończono próbę wczytania danych.")

def save_data(data, filename="data.json"):
    """Zapisywanie danych do pliku JSON."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Błąd zapisu: {e}")
    finally:
        print("Zakończono próbę zapisu danych.")