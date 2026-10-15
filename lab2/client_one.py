import os
import time
import errno
import sys


BUFOR = sys.argv[1] if len(sys.argv) > 1 else "bufor.txt"
PLIK_ODP = sys.argv[2] if len(sys.argv) > 1 else input("Nazwa pliku na odpowiedz: ").strip()

LOCKFILE = "plikZamkowy"
SLEEP_TIME = 3
ESC = "\x1b"

while True:  
    try:  
        fd = os.open(LOCKFILE, os.O_CREAT|os.O_EXCL|os.O_RDWR)  
        break;  
    except OSError as e:  
        if e.errno != errno.EEXIST:  
            raise   
        time.sleep(SLEEP_TIME)
        print("Serwer zajety prosze czekac")  
print("plik zamkowy utworzony") 


with open(BUFOR, os.O_RDWR) as f:
    f.write(CLIENT_FILE)
    while True:
        x = input("Podaj dane do zapisu (q aby przerwac): ") 
        if (x == "q"):
            break
        f.write(x)
    f.write(ESC)


