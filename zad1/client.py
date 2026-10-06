import sys
import time
DANE = "dane.txt"
WYNIKI = "wyniki.txt"

while True:
    x = input("Podaj liczbę (q aby przerwać): ").strip()
    if x == "q":
        sys.exit(0)
    try:
        x = int(x)
        break
    except ValueError:
        print("x musi być liczbą całkowitą")

open(WYNIKI, "w").close()

with open(DANE, "w") as f:
    f.write(f"{x}\n")

while True:
    with open(WYNIKI, "r+") as f:
        content = f.read()
        if content.endswith("\n"):
            f.seek(0)
            f.truncate()
        else:
            content = ""

    if content.strip():
        print("Wynik:", content.strip())
        break
    
    time.sleep(0.2)