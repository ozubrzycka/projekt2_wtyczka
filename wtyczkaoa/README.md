# Instrukcja obsługi Wtyczki do programu QGis
Wtyczka umożliwia wykonanie następujących operacji w programie QGIS:\
Operacje na dwóch punktach:
- Obliczenie różnicy wysokości.
- Obliczenie odległości.
- Wyznaczenie azymutu oraz azymutu odwrotnego.
Operacje na trzech lub więcej punktach:
- Obliczenie pola powierzchni.
Dodatkowe możliwości programu:
- Zliczanie zaznaczonych punktów.
- Wczytywanie pliku ze współrzędnymi punktów w układzie współrzędnych płaskich prostokątnych PL-1992 lub PL-2000.
- Czyszczenie wyników.

# Wymagania
- Python 3.11.5
- Biblioteki: math, PyQt5, os, qgis.utils, qgis.PyQt, qgis.core
- QGIS 3.34.7
- System operacyjny: Windows 11

# Jednostki obliczeń:
- Różnica wysokości: metry (m).
- Odległość: metry (m).
- Azymut i azymut odwrotny: stopnie dziesiętne (deg), grady (g).
- Pole powierzchni: metry kwadratowe (m²), kilometry kwadratowe (km²), ary (a), hektary (ha).

# Sposób użycia:
Wtyczka umożliwia wykonywanie wymienionych operacji w określonej wersji QGIS. Poniżej znajduje się opis funkcji każdego przycisku oraz instrukcja dotycząca wczytywania pliku.

- Pole wyboru "Aktualna warstwa"\
Pozwala wybrać warstwę, na której będą wykonywane operacje za pomocą wtyczki.
- Zlicz elementy\
Po naciśnięciu przycisku zwraca liczbę zaznaczonych elementów.
- Różnica wysokości\
Przeznaczony dla punktów z atrybutem wysokości oznaczonym jako "h".\
Po naciśnięciu przycisku wyświetla różnicę wysokości między zaznaczonymi punktami w metrach (m).
- Pole powierzchni\
Przed naciśnięciem przycisku należy wybrać jednostkę pola\
Następnie wyświetla pole powierzchni obszaru utworzonego przez zaznaczone punkty w wybranej z listy rozwijalnej jednostce.
- Odległość\
Wyświetla odległość między zaznaczonymi punktami w metrach (m).
- Azymut oraz Azymut odwrotny\
Wyświetla wartość azymutu między zaznaczonymi punktami w wybranej z listy rozwijalnej jednostce
- Wyczyść wyniki\
Usuwa wszystkie wyświetlane wyniki oraz komunikaty o wynikach lub błędach.
- Wczytaj plik\
Umożliwia wczytywanie plików .txt lub .csv zawierających współrzędne punktów.\
Współrzędne powinny być zapisane w formacie X,Y z separatorem dziesiętnym jako kropka i przecinkiem jako separator współrzędnych.\
Przykład dla układu PL-2000:

6505557.947,5698134.984\
6494228.235,5698070.407

Przykład dla układu PL-1992:

1201504.672, 698011.536

# Format plików wyjściowych
plik po zapisie 2 punkty\
Number of selected points: 2\
Coordinates of point number 1: X = 421378.051, Y = 374614.121\
Coordinates of point number 2: X = 440463.719, Y = 368503.516\
Distance between points (point id:1- id:2) is: 20040.016 [m]


plik po zapisie 3 punkty:\
Number of selected points: 3\
Coordinates of point number 1: X = 421378.051, Y = 374614.121\
Coordinates of point number 2: X = 440463.719, Y = 368503.516\
Coordinates of point number 3: X = 437051.935, Y = 380374.374


# Znane błędy i nietypowe zachowania:

Błąd po zapisaniu pliku z dwoma punktami:

TypeError: cannot unpack non-iterable NoneType object
Traceback (most recent call last):
  File "C:\Users/ozubr/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\wtyczkaoa\wtyczkaoa_dialog.py", line 252, in save_file_function\
    azimuth, reverse_azimuth = self.azimuth_function()  # Update: Added azimuth calculation\
TypeError: cannot unpack non-iterable NoneType object 


Błąd po zapisaniu pliku z 3 punktami: 

Error: Incorect Number of points selected








