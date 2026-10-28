import os
import time
import errno
import sys


BUFOR = sys.argv[1] if len(sys.argv) > 1 else "bufor.txt"
PLIK_ODP = sys.argv[2] if len(sys.argv) > 2 else input("Nazwa pliku na odpowiedz: ").strip()
PLIK_ODP = os.path.abspath(PLIK_ODP)

LOCKFILE = os.path.join(os.path.dirname(os.path.abspath(BUFOR)), "plikZamkowy")
SLEEP_TIME = 3
ESC = "\x1b"

linie = []
while True:
    x = input("Podaj linie tekstu (q aby zakonczyc): ")
    if x == "q":
        break
    linie.append(x)

try:
    os.remove(PLIK_ODP)
except FileNotFoundError:
    pass

while True:  
    try:  
        fd = os.open(LOCKFILE, os.O_CREAT|os.O_EXCL|os.O_RDWR) 
        os.close(fd) 
        break;  
    except OSError as e:  
        if e.errno != errno.EEXIST:  
            raise   
        time.sleep(SLEEP_TIME)
        print("Serwer zajety prosze czekac")   


with open(BUFOR, "w", encoding="utf-8") as f:
    f.write(PLIK_ODP + "\n")
    for l in linie:
        f.write(l + "\n")
    f.write(ESC)

print("Wyslano, czekam na odpowiedz...")

while True:
    try:
        with open(PLIK_ODP, encoding="utf-8") as f:
            odp = f.read()
        if odp.endswith(ESC):
            break
    except FileNotFoundError:
        pass
    time.sleep(0.5)

print("Odpowiedz serwera: ")
print(odp[:-1], end="")
os.remove(PLIK_ODP)