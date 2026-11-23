import os
import sys
import struct

FIFO = '/tmp/kolejka'

id = int(sys.argv[1])

moja_kolejka = '/tmp/kolejka_klienta_%d' % os.getpid()
os.mkfifo(moja_kolejka)

tresc = struct.pack('i', id) + moja_kolejka.encode()
fifo_out = os.open(FIFO, os.O_WRONLY)
os.write(fifo_out, struct.pack('i', len(tresc)) + tresc) 
os.close(fifo_out)

fifo_in = os.open(moja_kolejka, os.O_RDONLY)
dlugosc = struct.unpack('i', os.read(fifo_in, 4))[0]
odp = os.read(fifo_in, dlugosc).decode()
os.close(fifo_in)
os.unlink(moja_kolejka)

print('Klient %d: ID=%d -> %s' % (os.getpid(), id, odp))