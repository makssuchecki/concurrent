import signal
import sys
import time

import sysv_ipc

KLUCZ_WE = 11   
KLUCZ_WY = 12   
OPOZNIENIE = 2  

SLOWNIK = {
    "kot": "cat",
    "pies": "dog",
    "dom": "house",
    "drzewo": "tree",
    "książka": "book",
    "woda": "water",
    "słońce": "sun",
    "komputer": "computer",
}


dziala = True


def obsluga_sygnalu(signum, frame):
    global dziala
    dziala = False
    print("\nSerwer: otrzymałem sygnał %s" % signal.Signals(signum).name)


def main():
    kolejka_we = sysv_ipc.MessageQueue(KLUCZ_WE, sysv_ipc.IPC_CREAT)
    kolejka_wy = sysv_ipc.MessageQueue(KLUCZ_WY, sysv_ipc.IPC_CREAT)

    signal.signal(signal.SIGINT, obsluga_sygnalu)
    signal.signal(signal.SIGTERM, obsluga_sygnalu)

    print("Serwer: kolejki %d (we) i %d (wy) gotowe, czekam na zapytania" % (KLUCZ_WE, KLUCZ_WY))
    try:
        while dziala:
            try:
                dane, pid = kolejka_we.receive(True, 0)   # typ 0 = dowolny komunikat
            except sysv_ipc.Error:
                break
            slowo = dane.decode().strip()
            print("Serwer: od %d odebrałem '%s' (w kolejce czeka jeszcze: %d)"
                  % (pid, slowo, kolejka_we.current_messages))

            if slowo.lower() == "stop":
                print("Serwer: otrzymałem 'stop' od %d" % pid)
                break

            time.sleep(OPOZNIENIE)
            odpowiedz = SLOWNIK.get(slowo.lower(), "Nie znam takiego słowa")
            kolejka_wy.send(odpowiedz.encode(), True, pid)
            print("Serwer: do %d wysłałem '%s'" % (pid, odpowiedz))
    finally:
        for k in (kolejka_we, kolejka_wy):
            try:
                k.remove()
            except sysv_ipc.ExistentialError:
                pass
        print("Serwer: usunąłem obie kolejki, koniec pracy")


if __name__ == "__main__":
    main()
