Treść zadania:
Przedmiotem analizy jest tablica mieszająca: tablica przechowuje rekordy zawierające napisy.
Długość tablicy jest ograniczona arbitralnie przez pewną stałą K. Dla danego napisu sobliczamy k=M(s),
gdzie M() jest funkcją mieszającą i umieszczamy strukturę reprezentującąnapis w tablicy mieszającej: H[k].
W  przypadku  kolizji  funkcji  mieszającej  (H[k]  zajęte)  reprezentujące  napis sstruktury  danych zapisywane  są
w  sposób  alternatywny  zobacz  warianty).Przedmiotem  implementacji  powinno być: dodanie i usunięcie elementów w H[].
Wybór funkcji mieszającej M(s) należy do  decyzji  projektanta -ale patrz wariant 3.

Testy  przeprowadzić  dla:  sztucznie  wygenerowanych  słów,  generator  ma  posługiwać  się  tablicą prawdopodobieństw
wystąpienia  danej  litery  na  początku  slowa  (początek  słowa)  oraz  litery  po poprzedzającej  literze
(spacja,  kropka,  przecinek,  itp.  traktowane  są  jako  litera  specjalna  "koniec słowa").
Prawdopodobieństwa należy uzyskać z próbki tekstu polskiego.

[W13] W  przypadku  kolizji  funkcji mieszającej  reprezentujące napis struktury danych zapisywane
są w zrównoważonym drzewie binarnym, któregokorzeńto H[k].
[W21] Zastosować  jedną  funkcję  mieszającą;  dodatkowo  przeprowadzić  analizę  dla
enumeracji  tablicy (wydobycia wszystkich elementów).