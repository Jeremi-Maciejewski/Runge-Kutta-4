To tak w celu dokumentowania pomysłów na implementację.

# Input modelu z zewnątrz programu
(tylko pod warunkiem, że ze zmiennym modelem)

Możnaby się bawić w jakiś JSON albo XML ale chyba to przesada tutaj, więc proponuję jakiś prosty customowy sposób zapisu w pliku konfiguracyjnym.
~Jeremi


# Funkcja implementująca sam algorytm

## Input
(tylko pod warunkiem, że ze zmiennym modelem)

Myślę, że możnaby podawać listę customowych obiektów reprezentujących każdy z czynników (zmiennych/cząsteczek):
 - definiujących funkcję na obliczenie danej zmiennej - może można by nawet podawać ją już napisaną, żeby model tylko wywoływał
 - oraz stan początkowy zmiennej

Do tego pewnie długość kroku, bo głupio wpisywać na twardo w funkcję.
~Jeremi


Update:
I tak zrobiłem już klasę do tych obiektów ('Reagent'), bo uznałem, że przydadzą się też jako input do rysowania wykresu - więc chyba użyjemy tak czy tak, nie zaszkodzą.
~Jeremi


## Implementacja

## Output


# Wizualizacja
(najwyraźniej mają być wykresy)

Matplotlib + pyplot i proste wykresy liniowe, I guess?
~Jeremi

## Input
Jeden lub lista obiektów, o których wspomniałem przy inpucie do implementacji (zapisują zmiany odczynnika w czasie)(class Reagent)
~Jeremi


# Kompilacja
Korzystałem kiedyś z biblioteki pyinstaller do tego, wydaje mi się, że powinna być ok do tego zastosowania.
Nie pamiętam już jak dokładnie to działało ale zasadniczo trzeba było tylko zrobić plik konfiguracyjny i puścić program, który kompiluje...
~Jeremi
