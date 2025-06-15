# Moduł wizualizacji danych
import matplotlib.pyplot as plt

def plot_rent_distribution(pokoje):
    """Tworzenie histogramu rozkładu czynszów."""
    rents = [p.czynsz for p in pokoje]
    plt.hist(rents, bins=10, edgecolor="black")
    plt.title("Rozkład czynszu pokoi")
    plt.xlabel("Czynsz (zł)")
    plt.ylabel("Liczba pokoi")
    plt.savefig("rent_distribution.png")
    plt.show()