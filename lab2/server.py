import os
import time

BUFOR = os.path.abspath("bufor.txt")
LOCK = os.path.join(os.path.dirname(BUFOR), "plikZamkowy")
ESC = "\x1b"

print("Serwer aktywny")

while True:
    try:
        with open(BUFOR, "r+", encoding="utf-8") as f:
            content = f.read()
            if content.endswith(ESC):
                f.seek(0)
                f.truncate()
            else:
                content = ""
    except FileNotFoundError:
        content = ""

    if not content:
        time.sleep(0.5)
        continue

    file_name, _, tekst = content[:-1].partition("\n")
    print(f"\nOd klienta ({file_name}):")
    print(tekst, end="")

    linie = []
    while True:
        x = input("Odpowiedz (q aby zakonczyc): ")
        if x == "q":
            break
        linie.append(x)

    with open(file_name, "w", encoding="utf-8") as f:
        for l in linie:
            f.write(l + "\n")
        f.write(ESC)

    try:
        os.remove(BUFOR)
    except FileNotFoundError:
        pass
    try:
        os.remove(LOCK)
    except FileNotFoundError:
        print("Brak pliku zamkowego do usuniecia")
    print("Odpowiedz wyslana, plik zamkowy usuniety")