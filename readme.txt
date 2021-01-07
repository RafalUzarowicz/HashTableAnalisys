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

Konwencje we/wy
----------------------------------------------------------------------------------------------------

Opis metody
----------------------------------------------------------------------------------------------------

Przewodnik po źródłach programu
----------------------------------------------------------------------------------------------------

Dodatkowe informacje o decyzjach projektowych
----------------------------------------------------------------------------------------------------