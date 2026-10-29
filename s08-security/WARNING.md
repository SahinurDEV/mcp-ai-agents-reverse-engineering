# WARNING: deliberately insecure teaching code

`poisoned_server.py`, `inject_note.sh` and `rugpull_server.py` are written to be attacked or to attack a client.
They only touch files inside this folder (a fake `secrets.txt`) and never send data off the machine.
Do not install them in a real host, do not publish them as useful servers, and do not adapt them against others.
