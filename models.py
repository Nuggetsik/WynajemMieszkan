# Moduł z klasami dla systemu zarządzania wynajmem
from functools import reduce
import time


def log_execution_time(func):
    """Dekoder do rejestrowania czasu wykonania metody."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Metoda {func.__name__} została wykonana w {time.time() - start_time:.2f} sek.")
        return result

    return wrapper


class Najemca:
    """Klasa reprezentująca najemca."""

    def __init__(self, imie, nazwisko, email):
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email

    def to_dict(self):
        """Konwersja obiektu dzierżawcy na słownik."""
        return {
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "email": self.email
        }


class Pokoj:
    """Podstawowa klasa dla pokoju."""

    def __init__(self, numer, czynsz, najemca=None, lokalizacja=(0, 0)):
        assert czynsz > 0, "Czynsz musi być dodatni!" # Dodaj czek
        self.numer = numer
        self.czynsz = czynsz
        self.najemca = najemca
        self.lokalizacja = lokalizacja  # Krotka dla współrzędnych

    def to_dict(self):
        """Konwersja obiektu pokoju do słownika."""
        return {
            "numer": self.numer,
            "czynsz": self.czynsz,
            "najemca": self.najemca.to_dict() if self.najemca else None,
            "lokalizacja": self.lokalizacja
        }


class PremiumPokoj(Pokoj):
    """Ocena za pokoje premium z dodatkowymi udogodnieniami."""

    def __init__(self, numer, czynsz, najemca=None, lokalizacja=(0, 0), udogodnienia=None):
        super().__init__(numer, czynsz, najemca, lokalizacja)
        self.udogodnienia = udogodnienia or []

    def to_dict(self):
        """Konwersja obiektu pokoju premium na słownik."""
        data = super().to_dict()
        data["udogodnienia"] = self.udogodnienia
        return data


class App:
    """Główna klasa aplikacji do zarządzania wynajmem."""

    def __init__(self, filename):
        from utils import load_data
        self.data = load_data(filename)
        self.pokoje = self.load_pokoje()
        self.numbers_set = set(p.numer for p in self.pokoje)  # Wiele numerów pokoi

    def load_pokoje(self):
        """Ładowanie pokoi z danych JSON."""
        pokoje_data = self.data.get("pokoje", [])
        pokoje = []
        for p in pokoje_data:
            najemca_data = p.get("najemca")
            najemca = Najemca(**najemca_data) if najemca_data else None
            lokalizacja = tuple(p.get("lokalizacja", (0, 0)))  # Кортеж
            if p.get("udogodnienia"):
                pokoje.append(PremiumPokoj(p["numer"], p["czynsz"], najemca, lokalizacja, p["udogodnienia"]))
            else:
                pokoje.append(Pokoj(p["numer"], p["czynsz"], najemca, lokalizacja))
        return pokoje

    @log_execution_time
    def run(self):
        """Uruchamianie głównego menu aplikacji."""
        print("=== System zarządzania wynajmem mieszkań ===")
        self.menu()

    def menu(self):
        """Menu główne z wyborem operacji."""
        while True:
            print("\n1. Pokaż pokoje")
            print("2. Filtruj wg czynszu")
            print("3. Zapisz")
            print("4. Wyjście")
            print("5. Dodaj pokój")
            print("6. Edytuj pokój")
            print("7. Pokaż statystyki (rekurencja)")
            print("8. Pokaż wizualizację")
            choice = input("> ")
            if choice == "1":
                self.show_pokoje()
            elif choice == "2":
                self.filter_czynsz()
            elif choice == "3":
                self.save()
            elif choice == "4":
                break
            elif choice == "5":
                self.add_pokoj()
            elif choice == "6":
                self.edit_pokoj()
            elif choice == "7":
                print(f"Pomieszczenia zapasowe: {self.count_free_rooms_recursive(self.pokoje)}")
            elif choice == "8":
                self.visualize_data()
            else:
                print("Nieprawidłowy wybór!")

    def add_pokoj(self):
        """Dodanie nowego pomieszczenia."""
        try:
            numer = int(input("Numer pokoju: "))
            assert numer not in self.numbers_set, "Pokój o tym numerze już istnieje!"
            czynsz = float(input("Czynsz (zł): "))
            assert czynsz > 0, "Czynsz musi być dodatni!"
            lokalizacja_x = float(input("Koordynata X: "))
            lokalizacja_y = float(input("Koordynata Y: "))
            is_premium = input("Czy pokój jest premium? (t/n): ").lower() == "t"

            najemca = None
            if input("Czy pokój ma najemcę? (t/n): ").lower() == "t":
                imie = input("Imię najemcy: ")
                nazwisko = input("Nazwisko najemcy: ")
                email = input("Email najemcy: ")
                najemca = Najemca(imie, nazwisko, email)

            if is_premium:
                udogodnienia = input("Udogodnienia (oddzielone przecinkami): ").split(",")
                nowy_pokoj = PremiumPokoj(numer, czynsz, najemca, (lokalizacja_x, lokalizacja_y), udogodnienia)
            else:
                nowy_pokoj = Pokoj(numer, czynsz, najemca, (lokalizacja_x, lokalizacja_y))

            self.pokoje.append(nowy_pokoj)
            self.numbers_set.add(numer)
            print("Pokój dodany.")
        except (ValueError, AssertionError) as e:
            print(f"Błąd danych wejściowych: {e}")

    def edit_pokoj(self):
        """Edytowanie istniejącego pokoju."""
        try:
            numer = int(input("Numer pokoju do edycji: "))
            assert numer in self.numbers_set, "Pokój o tym numerze nie istnieje!"
            for pokoj in self.pokoje:
                if pokoj.numer == numer:
                    czynsz = input(f"Nowy czynsz (obecny: {pokoj.czynsz} zł, Enter aby pominąć): ")
                    if czynsz:
                        pokoj.czynsz = float(czynsz)
                    if input("Czy zmienić najemcę? (t/n): ").lower() == "t":
                        imie = input("Imię najemcy: ")
                        nazwisko = input("Nazwisko najemcy: ")
                        email = input("Email najemcy: ")
                        pokoj.najemca = Najemca(imie, nazwisko, email)
                    if isinstance(pokoj, PremiumPokoj):
                        udogodnienia = input("Nowe udogodnienia (oddzielone przecinkami, Enter aby pominąć): ")
                        if udogodnienia:
                            pokoj.udogodnienia = udogodnienia.split(",")
                    print("Pokój zaktualizowany.")
                    break
        except (ValueError, AssertionError) as e:
            print(f"Błąd: {e}")

    def show_pokoje(self):
        """Wyświetlanie wszystkich pomieszczeń."""
        if not self.pokoje:
            print("Brak pokoi w systemie.")
        for pokoj in self.pokoje:
            print(f"Pokój {pokoj.numer}, Czynsz: {pokoj.czynsz} zł, Lokalizacja: {pokoj.lokalizacja}")
            if isinstance(pokoj, PremiumPokoj):
                print(f"  Udogodnienia: {', '.join(pokoj.udogodnienia)}")
            if pokoj.najemca:
                print(f"  Najemca: {pokoj.najemca.imie} {pokoj.najemca.nazwisko}")

    def filter_czynsz(self):
        """Filtrowanie pokoi według czynszu przy użyciu lambda i filtra."""
        try:
            limit = float(input("Podaj maksymalny czynsz: "))
            # Korzystanie z filtrów i lambda
            znalezione = list(filter(lambda p: p.czynsz <= limit, self.pokoje))
            if not znalezione:
                print("Brak pokoi w podanym limicie.")
            for p in znalezione:
                print(f"Pokój {p.numer}, Czynsz: {p.czynsz} zł")
        except ValueError:
            print("Nieprawidłowa kwota.")

    def count_free_rooms_recursive(self, pokoje, index=0):
        """Rekursywne zliczanie dostępnych pokoi."""
        if index >= len(pokoje):
            return 0
        return (1 if pokoje[index].najemca is None else 0) + self.count_free_rooms_recursive(pokoje, index + 1)

    def visualize_data(self):
        """Wizualizacja danych przy użyciu matplotlib."""
        from visualization import plot_rent_distribution
        plot_rent_distribution(self.pokoje)

    @log_execution_time
    def save(self, filename="data.json"):
        """Zapisywanie danych w formacie JSON."""
        from utils import save_data
        pokoje_dict = list(map(lambda p: p.to_dict(), self.pokoje))  # Korzystanie z mapy
        self.data["pokoje"] = pokoje_dict
        save_data(self.data, filename)
        print("Dane zapisane.")

    def apply_function_to_rents(self, func):
        """Zastosowanie przeniesionej funkcji do płatności leasingowych."""
        return reduce(lambda acc, p: acc + func(p.czynsz), self.pokoje, 0)