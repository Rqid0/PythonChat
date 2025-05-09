import socket
import threading
import os
from cryptography.fernet import Fernet

#Informacje o serverze
SERVER_IP = "192.168.100.158"
SERVER_PORT = 50505

#Flagi wiadomości
FLAGA_WIADOMOSC = b'\x01'
FLAGA_KLUCZ = b'\x02'

#Klucz używany do szyfrowania
klucz = Fernet.generate_key()


def reciveMsg(sock):
    global klucz
    while True:
        odpowiedz = sock.recv(8192)
        if not odpowiedz:
            return
        if odpowiedz[1:].decode(errors="ignore") == "Ta nazwa jest już zajęta":
            print(odpowiedz[1:].decode(errors="ignore"))
            sock.close()
            os._exit(0)
        flaga = odpowiedz[0:1]
        if flaga == FLAGA_WIADOMOSC:
            wiadomosc = Fernet(klucz).decrypt(odpowiedz[1:]).decode()
            print(wiadomosc)

        elif flaga == FLAGA_KLUCZ:
            klucz = odpowiedz[1:]
        else:
            print("Otrzymano błędną flage wiadomosci.")
            return 1

def startClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    nazwa = input("Podaj nazwę użytkownika: ")
    sock.send(nazwa.encode())
    threading.Thread(target=reciveMsg,  args=(sock,), daemon=True).start()

    sock.send(FLAGA_KLUCZ+klucz)

    while True:
        try:
            wiadomosc = Fernet(klucz).encrypt(input("Wyślij: ").encode())
            odpowiedz = FLAGA_WIADOMOSC+wiadomosc
            sock.send(odpowiedz)
        except:
            break

startClient()