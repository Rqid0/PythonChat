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

def loadKey():
    try:
        with open("wspolnyklucz.key", "rb") as keyFile:
            return keyFile.read()
    except FileNotFoundError:
        print("Plik z kluczem nie istnieje!")
        exit()

klucz = loadKey()

session = PromptSession()

def reciveMsg(sock):
    asyncio.set_event_loop(asyncio.new_event_loop())

    while True:
        try:
            odpowiedz = sock.recv(8192)
            if not odpowiedz:
                return

            try:
                usernameEndIdx = odpowiedz.find(b": ")
                if usernameEndIdx != -1:
                    username = odpowiedz[:usernameEndIdx].decode()
                    encrypted_message = odpowiedz[usernameEndIdx + 2:]

                    wiadomosc = Fernet(klucz).decrypt(encrypted_message).decode()

                    print(f"{username}: {wiadomosc}")

                    run_in_terminal(lambda: print(f"\n{username}: {wiadomosc}", end='', flush=True))
                else:
                    print("[ERROR] Nieprawidłowy format wiadomości")
            except Exception as e:
                run_in_terminal(lambda: print(f"\n[Błąd deszyfrowania] {e}", end='', flush=True))
        except Exception as err:
            run_in_terminal(lambda: print(f"\n[Błąd odbierania danych] {err}", end='', flush=True))



def startClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    nazwa = input("Podaj nazwę użytkownika: ")
    sock.send(nazwa.encode())
    threading.Thread(target=reciveMsg, args=(sock,), daemon=True).start()

    with patch_stdout():
        while True:
            try:
                wiadomosc = session.prompt("Ty: ")
                zaszyfrowana = Fernet(klucz).encrypt(wiadomosc.encode())
                sock.send(zaszyfrowana)
            except (KeyboardInterrupt, EOFError):
                break

startClient()