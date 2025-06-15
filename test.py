# Moduł testów jednostkowych, funkcjonalnych, integracyjnych i brzegowych
import unittest
import timeit
from models import Najemca, Pokoj, PremiumPokoj, App
from utils import save_data, load_data
import os

class TestRentalSystem(unittest.TestCase):
    """Sala lekcyjna do testowania systemu wynajmu."""

    def setUp(self):
        """Inicjalizacja przed każdym testem."""
        self.najemca = Najemca("Jan", "Kowalski", "jan@example.com")
        self.pokoj = Pokoj(1, 1000.0, self.najemca, (10, 20))
        self.premium_pokoj = PremiumPokoj(2, 1500.0, None, (0, 0), ["WiFi", "TV"])
        self.app = App("test_data.json")
        self.app.pokoje = [self.pokoj, self.premium_pokoj]
        self.app.numbers_set = {1, 2}

        self.app.save("test_data.json")
        self.assertTrue(os.path.exists("test_data.json"), "Plik test_data.json nie został utworzony w setUp")

    def test_najemca_to_dict(self):
        """Test zamiany najemcy na słownictwo."""
        expected = {"imie": "Jan", "nazwisko": "Kowalski", "email": "jan@example.com"}
        self.assertEqual(self.najemca.to_dict(), expected)

    def test_pokoj_to_dict(self):
        """Test przekształcania pokoju w słownik."""
        expected = {
            "numer": 1,
            "czynsz": 1000.0,
            "najemca": self.najemca.to_dict(),
            "lokalizacja": (10, 20)
        }
        self.assertEqual(self.pokoj.to_dict(), expected)

    def test_premium_pokoj(self):
        """Test pokoju premium."""
        self.assertEqual(self.premium_pokoj.udogodnienia, ["WiFi", "TV"])

    def test_invalid_czynsz(self):
        """Test przypadku granicznego: ujemny czynsz."""
        with self.assertRaises(AssertionError):
            Pokoj(3, -1000.0)

    def test_invalid_numer(self):
        """Test przypadku granicznego: zduplikowany numer pokoju."""
        with self.assertRaises(AssertionError):
            self.app.add_pokoj_input(1, 1000.0, None, (0, 0), False, [])

    def test_functional_filter_czynsz(self):
        """Test funkcjonalny: filtrowanie według czynszu."""
        filtered = list(filter(lambda p: p.czynsz <= 1200.0, self.app.pokoje))
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].numer, 1)

    def test_integration_save_load(self):
        """Test integracji: zapisywanie i ładowanie danych."""
        try:
            self.app.save("test_data.json")
            self.assertTrue(os.path.exists("test_data.json"), "Plik test_data.json nie został utworzony")
            loaded_data = load_data("test_data.json")
            self.assertIn("pokoje", loaded_data, "Klucz 'pokoje' nie istnieje w pliku")
            self.assertEqual(len(loaded_data["pokoje"]), 2, "Nieprawidłowa liczba pokoi")
            self.assertEqual(loaded_data["pokoje"][0]["numer"], 1, "Nieprawidłowy numer pokoju")
        finally:
            if os.path.exists("test_data.json"):
                os.remove("test_data.json")

    def test_performance_save(self):
        """Test wydajności: czas przechowywania danych."""
        execution_time = timeit.timeit(lambda: self.app.save("test_data.json"), number=100)
        self.assertLess(execution_time, 1.0, "Zapisywanie jest zbyt wolne")

    def tearDown(self):
        """Sprzątanie po testach."""
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")

# Pomocnicza metoda testowania danych wejściowych
def add_pokoj_input(self, numer, czynsz, najemca, lokalizacja, is_premium, udogodnienia):
    """Metoda pomocnicza do symulacji add_pokoj."""
    assert numer not in self.numbers_set, "Pokój o tym numerze już istnieje!"
    assert czynsz > 0, "Czynsz musi być dodatни!"
    if is_premium:
        pokoj = PremiumPokoj(numer, czynsz, najemca, lokalizacja, udogodnienia)
    else:
        pokoj = Pokoj(numer, czynsz, najemca, lokalizacja)
    self.pokoje.append(pokoj)
    self.numbers_set.add(numer)

# Dodaj metodę do klasy App dla testów
App.add_pokoj_input = add_pokoj_input

if __name__ == "__main__":
    unittest.main()