"""Comprueba el puerto solicitado sin cerrar procesos ajenos."""
import socket
import sys

puerto = int(sys.argv[1])
if not 1024 <= puerto <= 65535:
    raise SystemExit('Puerto local invalido.')
with socket.socket() as servidor:
    try:
        servidor.bind(('127.0.0.1', puerto))
    except OSError:
        raise SystemExit(f'127.0.0.1:{puerto} esta ocupado. No se cerrara el proceso existente.')
print(f'Puerto disponible: http://127.0.0.1:{puerto}/')
