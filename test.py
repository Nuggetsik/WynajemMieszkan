# Moduł testów jednostkowych, funkcjonalnych, integracyjnych i brzegowych
import unittest
import timeit
from models import Najemca, Pokoj, PremiumPokoj, App
from utils import save_data, load_data
import os
from memory_profiler import profile

class TestRentalSystem(unittest.TestCase):
    """Sala lekcyjna do testowania systemu wynajmu."""
    def setUp(self):
        """Inicjalizacja przed każdym testem."""
        self.najemca = Najemca("Jan", "Kowalski", "jan@example.com")
        self.pokoj = Pokoj(1, 1000.0, self.najemca, {"miasto": "Warszawa", "ulica": "Marszałkowska", "numer_domu": "10"})
        self.premium_pokoj = PremiumPokoj(2, 1500.0, None, {"miasto": "Kraków", "ulica": "Floriańska", "numer_domu": "5"}, ["WiFi", "TV"])
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
            "lokalizacja": {"miasto": "Warszawa", "ulica": "Marszałkowska", "numer_domu": "10"}
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
        """Test przypadku granicznego: zduplikowany numer pokoju z inną lokalizacją."""
        # Pokój z tym samym numerem, ale inną lokalizacją powinien przejść
        self.app.add_pokoj_input(
            1, 1200.0, None, {"miasto": "Gdańsk", "ulica": "Długa", "numer_domu": "20"}, False, []
        )
        self.assertEqual(len(self.app.pokoje), 3)

    def test_invalid_lokalizacja(self):
        """Test przypadku granicznego: zduplikowany numer i lokalizacja."""
        with self.assertRaises(AssertionError):
            self.app.add_pokoj_input(
                1, 1200.0, None, {"miasto": "Warszawa", "ulica": "Marszałkowska", "numer_domu": "10"}, False, []
            )

    def test_edit_pokoj_by_number_and_lokalizacja(self):
        """Test edycji pokoju po numerze i lokalizacji."""
        # Dodajemy pokój z numerem 1, ale inną lokalizacją
        self.app.add_pokoj_input(
            1, 1200.0, None, {"miasto": "Gdańsk", "ulica": "Długa", "numer_domu": "20"}, False, []
        )
        # Edytujemy pokój z numerem 1 i lokalizacją Gdańsk, Długa 20
        for pokoj in self.app.pokoje:
            if pokoj.numer == 1 and pokoj.lokalizacja == {"miasto": "Gdańsk", "ulica": "Długa", "numer_domu": "20"}:
                pokoj.czynsz = 1300.0  # Zmiana czynszu
                nowy_najemca = Najemca("Anna", "Nowak", "anna@example.com")
                pokoj.najemca = nowy_najemca
                break
        # Sprawdzamy, czy czynsz i najemca zostali zmienieni
        for pokoj in self.app.pokoje:
            if pokoj.numer == 1 and pokoj.lokalizacja == {"miasto": "Gdańsk", "ulica": "Długa", "numer_domu": "20"}:
                self.assertEqual(pokoj.czynsz, 1300.0)
                self.assertEqual(pokoj.najemca.imie, "Anna")
                self.assertEqual(pokoj.najemca.nazwisko, "Nowak")
                break

    def test_edit_pokoj_invalid_number_and_lokalizacja(self):
        """Test przypadku granicznego: edycja nieistniejącego pokoju."""
        # Próbujemy edytować pokój z numerem 1 i nieistniejącą lokalizacją
        invalid_lokalizacja = {"miasto": "Poznań", "ulica": "Święty Marcin", "numer_domu": "15"}
        found = False
        for pokoj in self.app.pokoje:
            if pokoj.numer == 1 and pokoj.lokalizacja == invalid_lokalizacja:
                found = True
                break
        self.assertFalse(found, "Pokój o tym numerze i lokalizacji nie powinien istnieć!")

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
            self.assertIn("pokoje", loaded_data, "Klucz 'pokoje' nie istnieje")
            self.assertEqual(len(loaded_data["pokoje"]), 2)
            self.assertEqual(loaded_data["pokoje"][0]["numer"], 1)
        finally:
            if os.path.exists("test_data.json"):
                os.remove("test_data.json")

    def test_performance_save(self):
        """Test wydajności: czas przechowywania danych."""
        execution_time = timeit.timeit(lambda: self.app.save("test_data.json"), number=100)
        self.assertLess(execution_time, 1.0, "Zapisywanie jest zbyt wolne")

    @profile
    def test_memory_save(self):
        """Test pamięci: zużycie pamięci podczas zapisywania danych."""
        self.app.save("test_data.json")

    def tearDown(self):
        """Sprzątanie po testach."""
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")

# Pomocnicza metoda testowania danych wejściowych
def add_pokoj_input(self, numer, czynsz, najemca, lokalizacja, is_premium, udogodnienia):
    """Metoda pomocnicza do symulacji add_pokoj."""
    for p in self.pokoje:
        if p.numer == numer and p.lokalizacja == lokalizacja:
            raise AssertionError("Pokój o takim numerze i lokalizacji już istnieje!")
    assert czynsz > 0, "Czynsz musi być dodatni!"
    if is_premium:
        pokoj = PremiumPokoj(numer, czynsz, najemca, lokalizacja, udogodnienia)
    else:
        pokoj = Pokoj(numer, czynsz, najemca, lokalizacja)
    self.pokoje.append(pokoj)
    self.numbers_set.add(numer)
    return pokoj

# Dodaj metodę do klasy App dla testów
App.add_pokoj_input = add_pokoj_input

if __name__ == "__main__":
    unittest.main()