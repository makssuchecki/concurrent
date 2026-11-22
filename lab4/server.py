import os
import errno
import time
import sys
import signal
import struct

FIFO = "kolejka"

opoznienie = 5

baza = [
    (1, "Kowalski"),
    (2, "Nowak"),
    (3, "Zaorski"),
    (4, "Notecki"),
    (5, "Witkiewicz"),
    (6, "Polański"),
    (7, "Wójcik")
]

def szukaj(id):
    for (i, nazwisko) in baza:
        if i == id:
            return nazwisko
    return "Nie ma"

def ignoruj(sig, frame):
    print('Serwer: otrzymano sygnał %d - ignoruję' % sig)

def koniec(sig, frame):
    print("Serwer: otrzymano sygnał SIGUSR1 - koniec")
    os.close(fifo_in)
    os.close(fifo_out1)
    os.unlink(FIFO)
    sys.exit(0)

signal.signal(signal.SIGHUP, ignoruj)
signal.signal(signal.SIGTERM, ignoruj)
signal.signal(signal.SIGUSR1, koniec)

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if (oe.errno != errno.EEXIST):
        raise

fifo_in = os.open(FIFO, os.O_RDONLY)

fifo_out1 = os.open(FIFO, os.O_WRONLY | os.O_NDELAY)


while True:
    dlugosc = struct.unpack('i', os.read(fifo_in, 4))[0] 
    reszta = os.read(fifo_in, dlugosc)
    id = struct.unpack('i', reszta[:4])[0]
    sciezka = reszta[4:].decode()
    print('Serwer: zapytanie o ID=%d od %s' % (id, sciezka))

    time.sleep(opoznienie)

    odp = szukaj(id).encode()
    try:
        fifo_klienta = os.open(sciezka, os.O_WRONLY)
        os.write(fifo_klienta, struct.pack('i', len(odp)) + odp)  # jedno os.write
        os.close(fifo_klienta)
    except OSError as oe:
        print('Serwer: nie można odpowiedzieć klientowi: %s' % oe)