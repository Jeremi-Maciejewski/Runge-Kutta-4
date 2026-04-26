# Runge-Kutta-4

Implementacja metody Rungego-Kutty 4. rzędu (RK4) do symulacji modelu biologicznego (układ p53-MDM2-PTEN).

## Opis

Projekt umożliwia symulację dynamiki układu równań różniczkowych opisujących interakcje między białkami p53, MDM2 i PTEN.
Model (równania, parametry, wartości początkowe oraz scenariusze) definiowany jest w pliku YAML, a kod odpowiada za jego wczytanie i rozwiązanie metodą RK4.

## Struktura projektu

* `rk.py` - implementacja metody Rungego-Kutty 4. rzędu
* `config_loader.py` - wczytywanie i przetwarzanie modelu z pliku YAML
* `main.py` - uruchamianie symulacji i zapis wyników
* `configs/p53.yaml` - definicja modelu i scenariuszy

## Wymagania

* Python >= 3.11
* PyYAML
* matplotlib

Instalacja:

```bash
pip install pyyaml matplotlib
```

## Jak to działa

1. Model jest zapisany w YAML jako:

   * równania (stringi)
   * parametry
   * wartości początkowe
   * scenariusze (A, B, C, D)

2. `config_loader.py`:

   * podstawia parametry do równań
   * ustawia wartości początkowe
   * przygotowuje dane dla RK4

3. `rk.py`:

   * oblicza rozwiązanie numeryczne równań metodą RK4

4. Wyniki:

   * wykresy PNG dla każdej zmiennej
   * opcjonalnie plik CSV

## Uruchomienie

Jedno uruchomienie:

```bash
python main.py --config configs/p53.yaml --scenario A
```

Wszystkie scenariusze:

```bash
python main.py --config configs/p53.yaml --scenario all --out results --csv
```

## Scenariusze

Zdefiniowane w pliku YAML:

* A - brak uszkodzenia DNA
* B - uszkodzenie DNA
* C - nowotwór (PTEN off)
* D - terapia (siRNA)
