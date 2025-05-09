import socket
import threading
import os
from cryptography.fernet import Fernet

# Informacje o serwerze
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

def reciveMsg(sock):
    while True:
        odpowiedz = sock.recv(8192)
        if not odpowiedz:
            return

        komunikat = odpowiedz.decode(errors="ignore")
        if komunikat == "Ta nazwa jest już zajęta":
            print(komunikat)
            sock.close()
            os._exit(0)

        wiadomosc = Fernet(klucz).decrypt(odpowiedz).decode()
        print(wiadomosc)

def startClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    nazwa = input("Podaj nazwę użytkownika: ")
    sock.send(nazwa.encode())
    threading.Thread(target=reciveMsg,  args=(sock,), daemon=True).start()

    while True:
        try:
            wiadomosc = Fernet(klucz).encrypt(input("Ty: ").encode())
            sock.send(wiadomosc)
        except:
            break

startClient()
