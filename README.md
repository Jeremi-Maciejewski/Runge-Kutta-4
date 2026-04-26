# Runge-Kutta-4

Symulacja modeli biologicznych metodą Rungego-Kutty 4. rzędu.

## Używanie
Badany model należy skonfigurować poprzez stworzenie pliku w formacie [YAML](https://en.wikipedia.org/wiki/YAML).

Przykładowy plik (4 scenariusze dla modelu interakcji białek p53, MDM i PTEN) znajduje się w folderze 'configs'.

Choć zalecane jest korzystanie z programu poprzez wywołanie 'main.py' z użyciem interpretera języka Python, w sekcji 'Releases' dostępne są również gotowe do uruchomienia skompilowane wersje programu.

### Uruchomienie

Uruchomienie dla jednego scenariusza:
```bash
python main.py --config configs/p53.yaml --scenario A
```

Wszystkie scenariusze:
```bash
python main.py --config configs/p53.yaml --scenario all
```

Pełna lista opcji:
```bash
python main.py --help
```

### Kompilacja ze źródła
Program można skompilować za pomocą biblioteki języka Python [pyinstaller](https://pyinstaller.org/en/stable/) poprzez wykonanie poniższego polecenia:
```bash
pyinstaller build.spec
```

W rezultacie utworzony zostanie folder 'dist', w którym można znaleźć skompilowany program.

## Wymagania

* Python >= 3.11
* PyYAML
* matplotlib

Instalacja bibliotek:

```bash
pip install pyyaml matplotlib
```
