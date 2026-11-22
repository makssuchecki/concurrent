import os
import sys
import time

import sysv_ipc

KLUCZ_WE = 11
KLUCZ_WY = 12


def main():
    if len(sys.argv) < 2:
        print("Użycie: python3 klient.py <słowo> [liczba_zapytań]")
        sys.exit(1)
    slowo = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    pid = os.getpid()

    try:
        kolejka_we = sysv_ipc.MessageQueue(KLUCZ_WE)
        kolejka_wy = sysv_ipc.MessageQueue(KLUCZ_WY)
    except sysv_ipc.ExistentialError:
        print("Klient %d: kolejki nie istnieją, uruchom najpierw serwer" % pid)
        sys.exit(1)

    for i in range(1, n + 1):
        kolejka_we.send(slowo.encode(), True, pid)
        print("Klient %d: wysłałem zapytanie %d/%d: '%s'" % (pid, i, n, slowo))
        time.sleep(1)

    for i in range(1, n + 1):
        try:
            dane, typ = kolejka_wy.receive(True, pid)
        except sysv_ipc.ExistentialError:
            print("Klient %d: serwer usunął kolejki, przerywam" % pid)
            sys.exit(1)
        print("Klient %d: odpowiedź %d/%d (typ %d): '%s' -> '%s'"
              % (pid, i, n, typ, slowo, dane.decode()))


if __name__ == "__main__":
    main()