import time 
import os 

BUFOR = "bufor.txt"
LOCK = "plikZamkowy"
ESC = "\x1b"
print("Serwer aktywny")

while True:
    try: 
        with open(BUFOR, "r+") as f:
            content = f.read()
            if content.endswith(ESC):
                content.seek(0)
                content.truncate()
            else:
                content = ""
    except FileNotFoundError:
        content=""

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

    with open(file_name, "w") as f:
        for l in linie:
            f.write(l + "\n")
        f.write(ESC)

    os.remove(LOCK)
    print("Odpowiedz wyslana")
