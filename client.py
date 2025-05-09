import socket
import threading
import os
from cryptography.fernet import Fernet

SERVER_IP = "192.168.100.158"
SERVER_PORT = 50505

def reciveMsg(sock):
    while True:
        odpowiedz = sock.recv(1024).decode()
        if odpowiedz == "Ta nazwa jest już zajęta":
            print(odpowiedz)
            sock.close()
            os._exit(0)
        else:
            print(odpowiedz)
def startClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    nazwa = input("Podaj nazwę użytkownika: ")
    sock.send(nazwa.encode())
    threading.Thread(target=reciveMsg,  args=(sock,), daemon=True).start()

    while True:
        try:
            wiadomosc = input("Wyślij: ")
            sock.send(wiadomosc.encode())
        except:
            break

startClient()