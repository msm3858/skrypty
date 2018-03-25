###############################################################################
## IMPORT NIEZBĘDNYCH BIBLIOTEK
## WSZYSTKIE UŻYTE BIBLIOTEKI W SKRYPCIE POWINNY BYĆ DOŁĄCZONE WRAZ Z PYTHONEM
###############################################################################
import os
import re
import datetime
import sys
from collections import Counter
from multiprocessing.dummy import Pool as ThreadPool 
poczatek = datetime.datetime.now()
print(str(poczatek))
###############################################################################
## WYWOŁANIE SKRYPTU ORAZ OPIS DZIAŁANIA PROGRAMU
##############################################################################
print ("Rozpoczynam pracę skryptu: " + sys.argv[0])
numArgs = len(sys.argv)
###############################################################################
## OPIS PROGRAMU DLA 1 ARGUMENTU
##############################################################################
if numArgs == 2:
    if sys.argv[1] == 'help':
        print ("Można wprowadzić parametry dla skryptu wywołując go poprzez: python3 "+ sys.argv[0] + "nazwa_pliku.txt sciezka_do_pliku")
        print("np dla windows: python "+ sys.argv[0]+" NP_z_RN_bez_C_posortowane.txt C:\\Users\\marcinso\\Desktop\\programy Python\\obróbka numerów\\nowe\\")
        print("albo dla linux: python3 "+ sys.argv[0]+" NP_z_RN_bez_C_posortowane.txt /home/user/path/to/script/")
        print("można wywołać skrypt także bez podania ścieżki, jeśli plik znajduje się w tym samym folderze, co skrypt.")
        sys.exit()
    path = os.getcwd()
    print("Podano nazwę pliku do sprawdzenia: " + sys.argv[1] + " bez podania ścieżki do pliku")
    plik = os.path.join(path,sys.argv[1])
    if os.path.isfile(plik):
        print("Znaleziono plik")
        print("Nastąpi odczyt danych z pliku: "+plik)
    else:
        print("Nie ma pliku w obecnym folderze")
    try:
        numberfile = open(plik)
    except:
        sys.exit()
###############################################################################
## OPIS PROGRAMU DLA 2 ARGUMENTÓW
##############################################################################
elif numArgs == 3:
    path = sys.argv[2]
    plik = os.path.join(path,sys.argv[1])
    if os.path.exists(path):
        print("Znaleziono oraz zmieniono folder")
    else:
        print("ścieżka nie istnieje")
        sys.exit()
    if os.path.isfile(plik):
        numberfile = open(plik)
        print("Znaleziono plik")
        print("Nastąpi odczyt danych z pliku: "+plik)
    else:
        print("Nie ma pliku w danym folderze")
    try:
        numberfile = open(plik)
    except:
        sys.exit()
###############################################################################
## OPIS PROGRAMU DLA BRAKU ARGUMENTÓW
##############################################################################
else:
	
    print("Nie podano nazwy pliku w wywołaniu skryptu ani ścieżki. Jeśli chcesz określić te parametry, a nie wiesz jak wywołaj skrypt:")
    print("python3 " + sys.argv[0]+" help")
    input("Wciśnij klawisz, aby kontynuować działanie skryptu... ")
    print("Jeśli chcesz przerwać działanie programu naciśnij CTRL+C")
    plik = "NP_z_RN_bez_C_posortowane.txt"
    path = os.getcwd()
    plik = os.path.join(path,plik)
    print("Skrypt będzie szukał pliku: " + plik)
if os.path.isfile(plik):
    print("Znaleziono plik")
    print("Odczyt danych z pliku: "+plik)
else:
    print("Nie ma pliku w obecnym folderze")
try:
	numberfile = open(plik)
except:
	sys.exit()
###############################################################################
## POCZĄTEK DZIAŁANIA SKRYPTU
##############################################################################
print("Wejście do pliku")
numberfile = open(plik)
print("Odczyt danych z pliku")
content = numberfile.read()
# Zwolnienie z pamięci otwartego pliku
numberfile.close()
print("Koniec pracy z plikiem")
###############################################################################
## USTAWIENIE PARAMETRÓW DZIAŁANIA PROGRAMU
##############################################################################
# Wyszukanie wszystkich numerów z pliku.
print("Utworzenie wyrażenia regularnego składającego się z 9-ciu liczb")
numery = re.compile(r'\d+')
print("Wczytanie do tablicy wszystkich znalezionych numerów")
wszystkie_numery = numery.findall(content)
ilosc_wszystkich = len(wszystkie_numery)
# Zwolnienie z pamięci zawartości pliku.
content = None
# Utworzenie pliku logu z działania programu.
lognazwa = 'log.txt'
logplik = open(lognazwa,'w')
tekst = "Czas rozpoczęcia działania skryptu: " + str(poczatek)+'\n'
logplik.write(tekst)
# Utworzenie pustej tablicy zawierającej gotowe prefiksy
tymczasowe_prefiksy = []
gotowe_prefiksy = []
i_piecio = 0
i_szescio = 0
i_siedmio = 0
i_osmio = 0
# Koniec szukania numerów z tekstu. Numery wpisane do tablicy: wszystkie_numery.
tekst = "Znaleziono: " + str(len(wszystkie_numery)) +" numerów\n\n"
print(tekst)
logplik.write(tekst+'\n')
###############################################################################
## ROZPOCZĘCIE OBRÓBKI NUMERÓW DLA POSZUKIWANIA PREFIKSÓW
##############################################################################
for x in range (-4,0):
	wstepne = []
	numery_do_usuniecia = []
	# Utworzenie iteratora liczącego ilość prefiksów.
	i_zakres = 0
	if x == -4:
		zakresik = 'pięcio'
		zliczone = 10000
	elif x == -3:
		zakresik = 'szescio'
		zliczone = 1000
	elif x == -2:
		zakresik = 'siedmio'
		zliczone = 100
	elif x == -1:
		zakresik = 'ośmio'
		zliczone = 10
	#elif x == 0:
	#	zakresik = 'dziewięcio'
	#	zliczone = 1
	else:
		zakresik = 'dziwny zakres'

	tekst = "Wyszukanie prefiksów "+ zakresik +"cyfrowych"
	print(tekst)
	# Pętla dodająca do tabeli: wstepne numery bez x ostatnich cyfr.
	for numer in wszystkie_numery:
		if x == 0:
			wstepne.append(numer)
		else:
			wstepne.append(numer[:x])		
	# Zliczenie wystąpień dla danych prefiksów z tabeli wstepne_szescio.
	zestaw = Counter(wstepne)
	# Jeżeli, któryś z numerów występuje 1000/100/10 razy w zależności od x, to skrypt dodaje dany numer jako prefiks do tablicy tymczasowe_prefiksy.
	for k,v in zestaw.items():
		if v == zliczone:
			# Zwiększenie iteratora prefiksów pięcionumerowych o 1.
			i_zakres +=1
			# Dodanie do tablicy tymczasowe_prefiksy prefiksu.
			tymczasowe_prefiksy.append(k)
#########################################
## OBRÓBKA ZNALEZIONYCH PREFIKSÓW
#########################################
print("Sprawdzanie tymczasowych prefiksów")
g = 0
ilosc_tymczasowych = len(tymczasowe_prefiksy)
for tpref in tymczasowe_prefiksy:
	g += 1
	print("sprawdzanie " + str(g) + "/" + str(ilosc_tymczasowych) +" prefiksów")
	if len(tpref)==14:
		gotowe_prefiksy.append(tpref)
		i_piecio += 1
	if len(tpref)==15:
		if tpref[0:14] in tymczasowe_prefiksy:
			continue
		else:
			gotowe_prefiksy.append(tpref)
			i_szescio += 1
	if len(tpref)==16:
		if tpref[0:15] in tymczasowe_prefiksy:
			continue
		elif tpref[0:14] in tymczasowe_prefiksy:
			continue
		else:
			gotowe_prefiksy.append(tpref)
			i_siedmio += 1
	if len(tpref)==17:
		if tpref[0:14] in tymczasowe_prefiksy:
			continue
		elif tpref[0:15] in tymczasowe_prefiksy:
			continue
		elif tpref[0:16] in tymczasowe_prefiksy:
			continue
		else:
			gotowe_prefiksy.append(tpref)
			i_osmio += 1

tekst = "Znaleziono: {0} prefiksów pięciocyfrowych, {1} prefiksów szesciocyfrowych, {2} prefiksów siedmiocyfrowych, {3} prefiksów ośmioznakowych.\n".format(i_piecio,i_szescio,i_siedmio,i_osmio)
print(tekst)
logplik.write(tekst)
pozostalo = ilosc_wszystkich-(i_piecio*10000+i_szescio*1000+i_siedmio*100+i_osmio*10)
logplik.close()
logplik = open(lognazwa,'a')
print("Wpisuję znalezione prefiksy do pliku 'prefiksy.txt'")
prefnazwa = 'prefiksy.txt'
prefplik = open(prefnazwa,'w')
for pr in gotowe_prefiksy:
	prefplik.write(pr+'\n')
prefplik.close()
tekst = "\nSzukam: {0} pozostałych numerów, dla których nie znalazłem żadnych prefiksów.\n".format(pozostalo)
print(tekst)
logplik.write(tekst)
########################################
## POZOSTAŁOŚCI
########################################
class Pozostale:
	def __init__(self,gotowe_prefiksy):
		self.gotowe_prefiksy = gotowe_prefiksy
		self.piatki = []
		self.szostki = []
		self.siodemki = []
		self.osemki = []
		for pref in self.gotowe_prefiksy:
			if len(pref) == 14:
				self.piatki.append(pref)
			elif len(pref) == 15:
				self.szostki.append(pref)
			elif len(pref) == 16:
				self.siodemki.append(pref)
			elif len(pref) == 17:
				self.osemki.append(pref)
	def numer_w_prefiksach(self,numer):
		if numer[:-4] in self.piatki:
			pass
		elif numer[:-3] in self.szostki:
			pass
		elif numer[:-2] in self.siodemki:
			pass
		elif numer[:-1] in self.osemki:
			pass 
		else:
			return numer
	def print_gotowe_prefiksy(self):
		print (self.gotowe_prefiksy)
pool = ThreadPool(16) 
pozostale = Pozostale(gotowe_prefiksy)
print("Rozpoczynam szukanie wielowątkowe")
pozostale_numery = pool.map(pozostale.numer_w_prefiksach,wszystkie_numery)
print("Skończyłem szukać, ostateczna obróbka tablicy ze znalezionymi gotowymi prefiksami")
for poz in pozostale_numery:
	if poz != None:
		gotowe_prefiksy.append(poz)
nazwapliku = 'wynik_caly.txt'
plik = open(nazwapliku,'w')

for pref in gotowe_prefiksy:
    plik.write(pref+'\n')
plik.close()
koniec = datetime.datetime.now()
tekst = "Czas zakończenia działania skryptu: " + str(koniec)+'\n'
logplik.write(tekst)
tekst = "Czas działania skryptu: "+str(koniec-poczatek)
logplik.write(tekst)
logplik.close()
input("Skończono wykonywanie programu. Wciśnij przycisk, aby zamknąć skrypt... ")