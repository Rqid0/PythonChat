import socket
import threading
import os
from cryptography.fernet import Fernet
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.application import run_in_terminal
import asyncio
import sys

SERVER_IP = "192.168.100.158"
SERVER_PORT = 50505

klucz = Fernet.generate_key()

session = PromptSession()

#funkcja obsługująca otrzymywanie wiadomości
def reciveMsg(sock):
    global klucz
    asyncio.set_event_loop(asyncio.new_event_loop())

    while True:
        try:
            odpowiedz = sock.recv(8192)
            if not odpowiedz:
                return

            try:
                znakRozdzielajacy = odpowiedz.find(b": ")
                if znakRozdzielajacy != -1:
                    username = odpowiedz[:znakRozdzielajacy].decode()
                    encrypted_message = odpowiedz[znakRozdzielajacy + 2:]

                    wiadomosc = Fernet(klucz).decrypt(encrypted_message).decode()

                    print(f"{username}: {wiadomosc}")

                    run_in_terminal(lambda: print(f"\n{username}: {wiadomosc}", end='', flush=True))
                else:
                    klucz = odpowiedz
            except Exception as e:
                run_in_terminal(lambda: print(f"\nBŁĄD DESZYFROWANIA {e}", end='', flush=True))
        except Exception as err:
            run_in_terminal(lambda: print(f"\nBŁĄD ODBIERANIA DANYCH {err}", end='', flush=True))


#funkcja rozpoczynająca pracę klienta
def startClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    nazwa = input("Podaj nazwę użytkownika: ")
    sock.send(nazwa.encode())
    threading.Thread(target=reciveMsg, args=(sock,), daemon=True).start()

    sock.send(klucz) #wyślij nowy klucz do servera

    with patch_stdout():
        while True:
            try:
                wiadomosc = session.prompt("Ty: ")
                zaszyfrowana = Fernet(klucz).encrypt(wiadomosc.encode())
                sock.send(zaszyfrowana)
            except (KeyboardInterrupt, EOFError):
                break

startClient()