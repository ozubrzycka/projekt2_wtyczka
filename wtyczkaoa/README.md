# Instrukcja obsługi Wtyczki do programu QGIS
Wtyczka umożliwia wykonanie następujących operacji w programie QGIS:\
Operacje na dwóch punktach:
- Obliczenie różnicy wysokości,
- Obliczenie odległości,
- Wyznaczenie azymutu oraz azymutu odwrotnego,
Operacje na trzech punktach:
- Obliczenie pola powierzchni.
Dodatkowe możliwości programu:
- Zliczanie zaznaczonych punktów,
- Wczytywanie pliku ze współrzędnymi punktów w układzie współrzędnych płaskich prostokątnych PL-1992 lub PL-2000,
- Czyszczenie wyników,
- zapisanie niektórych danych do pliku,
- Wyświetlenie współrzędnych wybranych punktów.

# Wymagania
- Python 3.11.5
- Biblioteki: math, PyQt5, os, qgis.utils, qgis.PyQt, qgis.core
- QGIS 3.34.7
- System operacyjny: Windows 11

# Zalecenia 
- pobranie wtyczki i skompresowanie do pliku ZIP
- instalacja wtyczki w programie QGIS z pliku zip przez: "Wtyczki" --> "Zarządzanie wtyczkami" --> "Insaluj z pliku ZIP"

# Jednostki obliczeń
- Różnica wysokości: metry (m).
- Odległość: metry (m).
- Azymut i azymut odwrotny: stopnie dziesiętne (deg), grady (g).
- Pole powierzchni: metry kwadratowe (m²), kilometry kwadratowe (km²), ary (a), hektary (ha).

# Sposób użycia
Wtyczka umożliwia wykonywanie wymienionych operacji w określonej wersji QGIS. Poniżej znajduje się opis funkcji każdego przycisku oraz instrukcja dotycząca wczytywania pliku.

- Pole wyboru "Aktualna warstwa"\
Wybiera aktywną warstwę z programu QGIS.
- Zlicz elementy\
Po naciśnięciu przycisku zwraca liczbę zaznaczonych elementów na aktywnej warstwie, przycisk działa niezależnie od ilości zaznaczonych punktów.
- Różnica wysokości\
Przeznaczony dla punktów z atrybutem wysokości oznaczonym jako "wysokosc", atrybut musi znajdować się na 20 miejscu, licząc od 0 w tabeli atrybutów warstwy. Muszą zostać zaznaczone dokładnie dwa punkty na warstwie. \
Po naciśnięciu przycisku wyświetla różnicę wysokości między zaznaczonymi punktami w metrach (m).
- Pole powierzchni\
Przed naciśnięciem przycisku należy wybrać jednostkę pola z listy wyboru oraz najlepiej sprawdzić czy na warstwie są zaznaczone 3 punkty, ponieważ tylko dla takiej liczby zostanie wykonana operacja.\
Następnie wyświetla pole powierzchni obszaru utworzonego przez zaznaczone punkty w wybranej z listy rozwijalnej jednostce.
- Odległość\
Wyświetla odległość między zaznaczonymi punktami w metrach (m). Muszą zostać zaznaczone dokładnie dwa punkty na warstwie.
- Azymut oraz Azymut odwrotny\
Wyświetla wartość azymutu między zaznaczonymi punktami w wybranej z listy rozwijalnej jednostce. Muszą zostać zaznaczone dokładnie dwa punkty na warstwie. Uwaga, każdy przycisk działa na azymut i azymut odwrotny: przykład - naciśnięcie przycisku Azymut powoduje obliczenie azymutu i azymutu odwrotnego, pokazują się dwie wartości w odpowiednich miejscach.
- Wyczyść wyniki\
Usuwa wszystkie wyświetlane wyniki oraz komunikaty o wynikach lub błędach. 
- Wczytaj plik\
Umożliwia wybranie pliku .txt lub .csv zawierających współrzędne punktów.\
Współrzędne powinny być zapisane w formacie X,Y z separatorem dziesiętnym jako kropka i spacją jako separator współrzędnych. Z wczytanym plikiem nie można nic więcej zrobić - wtyczka nie została do tego przystosowana. \
Przykład dla układu PL-2000:

6505557.947 5698134.984\
6494228.235 5698070.407

Przykład dla układu PL-1992:

1201504.672 698011.536
- Wyświetl współrzędne\
Naciśnięcie przycisku powoduje wyświetlenie wspólrzędnych w przystosowanym do tego oknie. Wyświetlane współrzędne - przykład:

Coordinates of point 1: X = 45678.910, Y = 123456.789\
Coordinates of point 2: X = 34578.910, Y = 987666.789

# Zapisanie wyników 
Zapisz wynik: Przycisk zapisuje wyniki do pliku oraz prosi o wybranie lokalizacji zapisywanego pliku oraz podanie nazwy dla zapisywanego pliku. Format plików wyjściowych - wtyczka nie zapisuje wszytskich obliczonych danych, tylko wybrane:
Plik po zapisie 2 punkty:\
Number of selected points: 2\
Coordinates of point number 1: X = 421378.051, Y = 374614.121\
Coordinates of point number 2: X = 440463.719, Y = 368503.516\
Distance between points (point id:1- id:2) is: 20040.016 [m]


Plik po zapisie 3 punkty:\
Number of selected points: 3\
Coordinates of point number 1: X = 421378.051, Y = 374614.121\
Coordinates of point number 2: X = 440463.719, Y = 368503.516\
Coordinates of point number 3: X = 437051.935, Y = 380374.374


# Znane błędy i nietypowe zachowania

Błąd po podaniu nazwy zapisywanego pliku i zapisaniu pliku z dwoma punktami. Plik się zapisuje w podanej lokalizacji, ale pojawia się poniższe okno z błędem:

TypeError: cannot unpack non-iterable NoneType object
Traceback (most recent call last):
  File "C:\Users/ozubr/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\wtyczkaoa\wtyczkaoa_dialog.py", line 252, in save_file_function\
    azimuth, reverse_azimuth = self.azimuth_function()  # Update: Added azimuth calculation\
TypeError: cannot unpack non-iterable NoneType object 


Błąd po podaniu nazwy zapisywanego pliku i zapisaniu pliku z trzema punktami. Plik się zapisuje w podanej lokalizacji, ale pojawia się poniższe okno z błędem:

Error: Incorect Number of points selected

Wtyczka zwraca bład po podaniu większej liczby punktów niż dopuszczalna dla wybranej operacji:
- pole: błąd przy podaniu innej liczby punktów niż 3
- wysokość, odległość, azymut i azymut odwrotny: błąd przy podaniu innej liczby punktów niż 2









