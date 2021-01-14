Zespół projektowy
----------------------------------------------------------------------------------------------------
Joanna Sokołowska, nr indeksu 289463
Rafał Uzarowicz, nr indeksu


Treść zadania
----------------------------------------------------------------------------------------------------
Przedmiotem analizy jest tablica mieszająca, przechowywująca rekordy zawierające napisy. Długość
tablicy jest ograniczona arbitralnie przez pewną stałą K. Dla danego napisu s obliczamy k=M(s), gdzie
M() jest funkcją mieszającą i umieszczamy strukturę reprezentującą napis w tablicy mieszającej: H[k].
W przypadku kolizji funkcji mieszającej reprezentujące napis s struktury danych
zapisywane są w zrównoważonym drzewie binarnym, którego korzeń to H[k] (W13).
Przedmiotem implementacji jest dodanie i usunięcie elementów w tablicy mieszającej.

Testy przeprowadzić dla: sztucznie wygenerowanych słów, generator ma posługiwać się tablicą
prawdopodobieństw wystąpienia danej litery na początku slowa (początek słowa) oraz litery po
poprzedzającej literze, (spacja, kropka, przecinek, itp. traktowane są jako litera specjalna "koniec
słowa"). Prawdopodobieństwa należy uzyskać z próbki tekstu polskiego.
Ponadto analiza będzie przeprowadzana również dla enumeracji tablicy (W21).


Aktywacja programu
----------------------------------------------------------------------------------------------------
Program można uruchomić z linii poleceń używając komendy:
python -m control.interface [flagi]

Za pomocą flag można wybrać jeden z 3 trybów wykonania programu, a także podać dodatkowe parametry.
Tryby uruchomienia są następujące:
1.  Tryb standardowy (opcja domyślna) - program oczekuje na dane na standardowym wejściu. Dla każdej
    z podanych instancji problemu z nich tworzy tablicę mieszającą i wypełnia ją
    podanymi kluczami, enumeruje elementy tablicy, wypisując je na standardowe wyjście i w losowej
    kolejności usuwa wszystkie elementy z drzewa. Nie są przeprowadzane pomiary czasu.
2.  Tryb standardowy z generacją danych - dla podanych wielkości problemu program generuje klucze
    losowe korzystając z modułu generacji tekstu, a następnie dla każdej
    instancji wykonuje działania analogiczne do trybu standardowego. Podobnie jak
    w trybie standardowym, tu również nie są przeprowadzane pomiary czasu. Format oczekiwanego wejścia
    jest zgodny z wyjściem modułu generatora tekstowego.
3.  Tryb testowy - program przeprowadza eksperymenty dla predefiniowanych lub wprowadzonych rozmiarów
    problemu (potrzebne dane są generowane z wykorzystaniem modułu generatora). Eksperymenty składają
    się z 3 pomiarów (dla dodawania klucza, usuwania i enumeracji wszystkich kluczy w tablicy mieszającej)
    i dla każdego rozmiaru powtarzane są 100-krotnie (wartość tę można zmienić z wykorzystaniem
    odpowiedniej flagi). Wyniki pomiarów dla każdego rozmiaru problemu są uśredniane, a następnie
    wyliczana jest ich zgodność z teoretyczną złożonością problemu. Dane (zarówno te zmierzone
    eksperymentalnie jak i ich porównanie z analizą teoretyczną) są wyświetlane na standardowym wyjściu
    w formie tabeli tekstowej.


Dostępne flagi:
-h --help            Wyświetla wszystkie możliwe flagi wraz z opisami ich zastosowania.
-test                Uruchom program w trybie testowym.
-gen                 Uruchom program w trybie standardowym z generacja danych.
-k K                 Arbitralna stała ograniczająca długość tabeli mieszającej, domyślnie k=50.
-r R                 Liczba powtórzeń eksperymentów, domyślnie r=100 (działa tylko dla trybu testowego).
--outfile OUTFILE    Nazwa pliku csv, w którym zostaną zapisane wyniki eksperymentów (tylko dla trybu
                     testowego).
--sizes [N....N]     Lista rozmiarów problemu, dla których ma zostać przeprowadzona analiza (tryb
                     testowy) lub wielkość instancji problemu, dla trybu standardowego z generacja danych.

Flagi związane z generacją kluczy:
--infile INFILE      Plik wejściowy na podstawie którego zostanie wygenerowana tablica prawdopodobieństw.
--prob-tbl PROB_TBL  Plik zawierający tablicę prawdopodobieństw
--url URL            Adres url do pliku tekstowego zawierającego tekst, na podstawie którego zostanie
                     wygenerowana tablica prawdopodobieństw.

Flagi gen i test są wzajemnie wykluczające, podobnie flagi inm prob-tbl i url.

Można odrębnie uruchomić również sam moduł generatora poleceniem:
python3 -m text.main [flagi]

Dostępne flagi
--infile INFILE      Plik wejściowy na podstawie którego zostanie wygenerowana tablica prawdopodobieństw.
--prob-tbl PROB_TBL  Plik zawierający tablicę prawdopodobieństw
--url URL            Adres url do pliku tekstowego zawierającego tekst, na podstawie którego zostanie
                     wygenerowana tablica prawdopodobieństw.
--outfile OUTFILE    Nazwa pliku tekstowego, w którym zostaną zapisane wygenerowane klucze.
-c C                 Liczba kluczy, które chce się wygenerować.
--sizes N [N...]     Lista rozmiarów problemu, dla których ma zostać przeprowadzona analiza (tryb
                     testowy) lub wielkość instancji problemu, dla trybu standardowego z generacja danych.


Konwencje we/wy
----------------------------------------------------------------------------------------------------
Wejście:
Jeśli program został uruchomiony w trybie standardowym to oczekuje on na wejście, gdzie każda instancja
problemu składa się z niepustych napisów rozdzielonych spacjami, a poszczególne instancje rozdzielone są
znakiem nowej linii. Koniec danych wejściowych powinien być sygnalizowany pustą instancją (tj. po
ostatniej niepusej instancji następują dwa znaki nowej linii przedzielone co najwyżej innymi znakami
białymi). Konwencja przyjęta dla wejścia jest zgodna ze standardowym wyjściem programu generującego.

Wyjście:
W trybach standardowym i standardowym z generacją danych program wyświetla na wyjściu standardowym
informacje o tym jakie obecnie dokonywane są operacje, o ich zakończeniu i tym, czy liczba elementów
w tablicy (lub liczba enumerowanych elementów) jest zgodna z oczekiwaniami.
W trybie testowym, ze względu na potencjalną czasochłonność wykonania, program wyświetla pasek postępu
dla każdego analizowanego rozmiaru problemu wraz z informacją o zakończeniu tego kroku. Po dokonaniu
wszystkich obliczeń program prezentuje wyliczone dane w formie 3 tabeli tekstowych (po jednej dla
każdego badanego elementu - enumeracji, dodawania i usuwania klucza).


Opis metody
----------------------------------------------------------------------------------------------------
Generacja tekstu
Na podstawie próbki tekstu generowana jest tablica prawdopodobieństw kolejnych wystąpień liter alfabetu
polskiego. Następnie generowane są instancje problemu (o zadanej wielkości) napis po napisie i litera
po literze. Wielkość instancji jest określana liczbą składających się na nią napisów. Do wybrania kolejnej
litery używane są liczby pseudolosowe generowane z wykorzystaniem biblioteki random. Po końcu generacji
wyniki są zapisywane do pliku lub wypisywane na standardowe wyjście zgodnie z przyjętą konwencją.

Realizacja tablicy mieszającej
Zgodnie z treścią zadania tablica mieszająca zrealizowana jest z wykorzystaniem dwóch struktur:
listy i zrównoważonego drzewa binarnego (drzewo AVL). Jeśli w danym elemencie listy realizującej tabelę
mieszającą miałby być zapisany drugi i kolejne klucze to zamiast tego wszystkie klucze zapisywane są w
drzewie binarnym o korzeniu będącym tym elementem listy.

Metodyka testowania
Testowaniu podlegają 3 operacje - dodawanie, enumeracja i usuwanie elementów z drzewa. Najpierw są generowane
klucze w potrzebnej ilości (o jeden większej niż rozmiar problemu), następnie tworzona jest tablica mieszająca,
do której dodawane są wszystkie wygenerowane klucze z wyjątkiem jednego. Mierzony jest czas enumeracji
wszystkich elementów tablicy, następnie czas dodania uprzednio zachowanego klucza do tablicy, potem
usuwany jest właśnie dodany klucz (w celu zachowania poprawnego rozmiaru problemu), a następnie mierzony jest
czas usunięcia losowego klucza w drzewie. Dla każdego rozmiaru problemu ten proces (poczynając od generacji kluczy)
powtarzany jest r razy (gdzie r jest parametrem linii poleceń, o domyślnej wartości 100), a wyniki są uśredniane,
aby możliwie dobrze wyeliminować czynnik losowy.


Przewodnik po źródłach
----------------------------------------------------------------------------------------------------
Projekt składa się z 3 modułów - control, hash i text.

Moduł control
Zawiera skrypt interface.py odpowiadający za tryby wykonania programu. Tu zdefiniowane są ich postacie,
obsługa wejścia i wyjścia, a także argumentów linii poleceń. Ten skrypt odpowiada również za tworzenie
struktur danych, wykonywanie na nich operacji i generowanie tekstu przy wykorzystaniu modułu generacji
(o ile została wybrana taka opcja). Zawiera też funkcje pomocnicze, ułatwiające realizację programu.

Moduł hash
Zawiera dwa pliki hash_table.py i binary_tree.py realizujące odpowiednio strukturę tabeli mieszającej
i drzewa binarnego (drzewo AVL). Zdefiniowane są tam klasy realizujące struktury danych oraz metody
dostępu do nich.

Moduł text
Zawiera dwa pliki generator.py i main.py. Plik generator.py definiuje klasę generatora tekstu wraz z
metodą generacji losowych napisów. Plik main.py odpowiada za obsługę argumentów linii poleceń, dzięki
czemu generator może być wykorzystywany niezależnie od modułu control. Jego działanie jest opisane
szczegółowo w dokumentacji końcowej.

Dodatkowe informacje
----------------------------------------------------------------------------------------------------
Ze względu na czasochłonność wykonywania testów program uruchomiony w trybie testowym okresowo zapisuje
dotychczas zgromadzone dane do tymczasowego pliku csv. Dzięki temu, jeśli program będzie musiał zostać
przerwany w trakcie obliczeń. Nazwa pliku ma format temp-[k]k-[r]r.csv, gdzie [k] i [r] są wartościami
zmiennych k i repetitions ustawianych przez argumenty linii poleceń. Plik tymczasowy jest usuwany przed
prezentacją wyników i jeśli została ustawiona flaga outfile wyniki końcowe wraz z analizą zgodności teorią
są zapisywane do podanego pliku.

Ponadto, aby urozmaicić czekanie na wykonanie się eksperymentów, program wyświetla paski postępu (oddzielny
dla każdego zadanego rozmiaru problemu).