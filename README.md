# Runge-Kutta-4

Symulacja modelu biologicznego (p53–MDM2–PTEN) metodą Rungego-Kutty 4. rzędu.

## Wymagania

* Python >= 3.11
* PyYAML
* matplotlib

Instalacja:

```bash
pip install pyyaml matplotlib
```

## Uruchomienie

Jedno uruchomienie:

```bash
python main.py --config configs/p53.yaml --scenario A
```

Wszystkie scenariusze:

```bash
python main.py --config configs/p53.yaml --scenario all --out results --csv
```

