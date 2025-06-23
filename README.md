Wynajem Mieszkan
Aplikacja do zarządzania wynajmem mieszkań napisana w języku Python. Umożliwia dodawanie, edytowanie, przeglądanie i filtrowanie pokoi (mieszkań) na podstawie czynszu. 
Projekt wykorzystuje programowanie obiektowe i funkcyjne, obsługę plików JSON oraz testy jednostkowe.

Opis projektu
Wynajem Mieszkan to system zarządzania wynajmem mieszkań, który pozwala użytkownikowi na:

Dodawanie nowych pokoi (zwykłych lub premium) z numerem, czynszem, lokalizacją i najemcą.
Edytowanie istniejących pokoi (czynsz, najemca, udogodnienia dla pokoi premium).
Filtrowanie pokoi według maksymalnego czynszu.
Wyświetlanie listy pokoi z szczegółami.
Zliczanie wolnych pokoi za pomocą rekurencji.
Wizualizację rozkładu czynszu za pomocą matplotlib.
Zapis i odczyt danych w formacie JSON.

Projekt został stworzony w ramach przedmiotu "Języki skryptowe" i łączy w sobie techniki programowania obiektowego, funkcyjnego oraz testowania oprogramowania.
Funkcjonalności

Dodawanie pokoi: Użytkownik może wprowadzić numer, czynsz, lokalizację (miasto, ulica, numer domu), dane najemcy oraz udogodnienia (dla pokoi premium).
Edytowanie pokoi: Możliwość zmiany czynszu, najemcy lub udogodnień po identyfikacji pokoju przez numer i lokalizację.
Filtrowanie pokoi: Filtrowanie pokoi na podstawie maksymalnego czynszu z użyciem funkcji filter i lambda.
Wizualizacja danych: Generowanie histogramu rozkładu czynszu za pomocą matplotlib.
Zapis danych: Dane są zapisywane w pliku data.json i wczytywane przy starcie aplikacji.
Testowanie: Kompleksowe testy jednostkowe, funkcjonalne, integracyjne i graniczne z użyciem unittest i memory_profiler.

Wymagania
Python 3.8 lub nowszy
Biblioteki:
matplotlib (do wizualizacji danych)
memory_profiler (do analizy zużycia pamięci w testach)

Użycie
Po uruchomieniu aplikacji (python main.py) wyświetli się menu tekstowe z opcjami:
=== System zarządzania wynajmem mieszkań ===
1. Pokaż pokoje
2. Filtruj wg czynszu
3. Zapisz
4. Wyjście
5. Dodaj pokój
6. Edytuj pokój
7. Pokaż statystyki (rekurencja)
8. Pokaż wizualizację
>

Przykład: Dodawanie pokoju
Wejście:
> 5
Numer pokoju: 1
Czynsz (zł): 1200
Miasto: Gdańsk
Ulica: Długa
Numer domu: 20
Czy pokój jest premium? (t/n): t
Czy pokój ma najemcę? (t/n): t
Imię najemcy: Anna
Nazwisko najemcy: Nowak
Email najemcy: anna@example.com
Udogodnienia (oddzielone przecinkami): WiFi,Balkon

Wyjście:
Pokój dodany.

Przykład: Edytowanie pokoju
Wejście:
> 6
Numer pokoju do edycji: 1
Miasto pokoju: Gdańsk
Ulica pokoju: Długa
Numer domu pokoju: 20
Nowy czynsz (obecny: 1200.0 zł, Enter aby pominąć): 1300
Czy zmienić najemcę? (t/n): t
Imię najemcy: Piotr
Nazwisko najemcy: Wiśniewski
Email najemcy: piotr@example.com
Nowe udogodnienia (oddzielone przecinkami, Enter aby pominąć): WiFi,TV,Balkon

Wyjście:
Pokój zaktualizowany.

Przykład: Filtrowanie pokoi
Wejście:
> 2
Podaj maksymalny czynsz: 1300

Wyjście:
Pokój 1, Czynsz: 1300.0 zł

Przykład: Błąd przy edycji nieistniejącego pokoju
Wejście:
> 6
Numer pokoju do edycji: 1
Miasto pokoju: Poznań
Ulica pokoju: Święty Marcin
Numer domu pokoju: 15

Wyjście:
Błąd: Pokój o tym numerze i lokalizacji nie istnieje!

Autorzy

Mykyta Lytvyn
Danylo Rushchak
