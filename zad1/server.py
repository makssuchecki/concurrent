import time 

DANE = "dane.txt"
WYNIKI = "wyniki.txt"

def func(x):
    return x*x*x

print("Serwer aktywny")

while True:
    with open(DANE, "r+") as f:
        content = f.read()
        if content.endswith("\n"):
            f.seek(0)
            f.truncate()
        else:
            content = ""

    if content.strip():
        try:
            result = str(func(int(content)))
        except ValueError:
            result = "To nie jest liczba calkowita"
        with open(WYNIKI, "w") as out:
            out.write(result + "\n")

    time.sleep(0.2)