
# Analiza wskaźnika MACD z wykorzystaniem danych giełdowych

Projekt polega na implementacji i analizie działania technicznego wskaźnika **MACD (Moving Average Convergence Divergence)**, który służy do identyfikacji momentów kupna i sprzedaży akcji. Został on wykorzystany do przeprowadzenia symulacji transakcji giełdowych dla trzech różnych spółek o odmiennych trendach rynkowych: Apple (AAPL), Nestlé (NESN) i Allegro (ALEP).

Projekt został wykonany w ramach zajęć **Metody Numeryczne**, implementacja została przeprowadzona w Pythonie.

## Czym jest MACD?

MACD to różnica dwóch wykładniczych średnich kroczących (EMA) – krótszej i dłuższej. W projekcie przyjęto:
- `Nshort = 12` – EMA krótkoterminowa,
- `Nlong = 26` – EMA długoterminowa,
- `Nsignal = 9` – EMA wskaźnika MACD (linia sygnałowa).

Przecięcia MACD i linii sygnałowej są interpretowane jako:
- **Kupno** – MACD przecina linię sygnałową od dołu,
- **Sprzedaż** – MACD przecina linię sygnałową od góry.

## Sprawozdanie

Szczegółowe opisy algorytmów, interpretacja wyników oraz wykresy znajdują się w pliku [MACD_MN1.pdf](./MACD_MN1.pdf).

## Wymagania

- Python 3.10+
- `pandas`
- `numpy`
- `matplotlib`

Można je zainstalować poleceniem:

```bash
pip install requirements.txt
```

## Uruchomienie

1. Umieść pliki danych w folderze `data/` (`AAPL.csv`, `NESN.csv`, `ALEP.csv`).
2. W pliku `main.py` zmień wartość `datachoice`:
   - `0` – Apple,
   - `1` – Nestlé,
   - `2` – Allegro.
3. Uruchom program: (możliwe, że będzie trzeba odkomentować niektóre fragmenty)

```bash
python main.py
```

W folderze `diagrams/` pojawią się wygenerowane wykresy.

## Co robi program?

- Oblicza wskaźniki EMA, MACD i linię sygnałową.
- Identyfikuje momenty przecięć (kupna/sprzedaży).
- Symuluje zachowanie portfela przy pełnych transakcjach w tych momentach.
- Generuje wykresy:
  - cen akcji z oznaczonymi punktami transakcji,
  - przebiegu MACD i SIGNAL,
  - wartości portfela,
  - liczby posiadanych akcji,
  - zysków i strat z każdej transakcji.

