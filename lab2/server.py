import time 
import os 

BUFOR = "bufor.txt"
LOCK = "plikZamkowy"
ESC = "\x1b"

print("Serwer aktywny")

while True:
    content = ""
    try: 
        with open(BUFOR, "r+", encoding="utf-8") as f:
            data = f.read()
            if data.endswith(ESC):
                content = data
                f.seek(0)
                f.truncate()
    except FileNotFoundError:
        pass

    if not content:
        time.sleep(0.5)
        continue

    file_name, _, tekst = content[:-1].partition("\n")
    print(f"od klienta {file_name}: ")
    print(tekst, end="")

    linie = []
    while True:
        x = input("Odpowiedz (q aby zakonczyc): ")
        if x == "q":
            break
        linie.append("q")

    with open(file_name, "w", encoding="utf-8") as f:
        for l in linie:
            f.write(l + "\n")
        f.write(ESC)

    try:
        os.remove(LOCK)
    except FileNotFoundError:
        pass
    print("Odpowiedz wyslana\n")
