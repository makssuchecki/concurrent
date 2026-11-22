import os
import sys

import sysv_ipc

KLUCZ_WE = 11

try:
    kolejka_we = sysv_ipc.MessageQueue(KLUCZ_WE)
except sysv_ipc.ExistentialError:
    print("Kolejka nie istnieje, serwer nie działa")
    sys.exit(1)

kolejka_we.send("stop".encode(), True, os.getpid())
print("Wysłałem 'stop' do serwera")
