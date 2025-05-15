import socket
import threading
import base64
from cryptography.fernet import Fernet

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 50505
clients = []


#funkcja sprawdzająca, czy wiadomość jest kluczem używanym do kodowania (bardzo małą szansa na pomyłke w przypadku normalnej wiadomości)
def isFernetKey(wiadomosc: str) -> bool:
    try:
        f = Fernet(wiadomosc)
        _ = f.encrypt(b"test")
        return True
    except Exception:
        return False

#funkcja obsługująca połączonych klientów
def handleClient(clientSocket, clientAdres):
    print(f"Nowy klient się połączył: {clientAdres}")
    try:
        nazwa = clientSocket.recv(8192).decode().strip()

        if any(c["name"] == nazwa for c in clients):
            clientSocket.send("Ta nazwa jest już zajęta".encode())
            clientSocket.close()
            return

        clients.append({"name": nazwa, "socket": clientSocket})
        print(f"{nazwa} dołączył.")

        while True:
            try:
                dane = clientSocket.recv(8192)
                if not dane:
                    break
                print(f"[{nazwa}] wysłał dane: {dane[:50]}...")

                for client in clients:
                    if client["socket"] != clientSocket:
                        try:
                            if(isFernetKey(dane)):
                                client["socket"].send(dane)
                            else:
                                client["socket"].send(f"{nazwa}: ".encode() + dane)
                        except Exception as e:
                            print(f"Nie udało się wysłać do {client['name']}: {e}")
            except:
                break

    except Exception as e:
        print(f"Błąd z klientem: {e}")
    finally:
        print(f"Klient: {clientAdres} się rozłączył")
        clientSocket.close()
        clients[:] = [c for c in clients if c["socket"] != clientSocket]

#funkcja rozpoczynająca pracę servera
def startServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print(f"Server nasłuchuje na {SERVER_IP}:{SERVER_PORT}")

    while True:
        clientSocket, clientAdres = server.accept()
        threading.Thread(target=handleClient, args=(clientSocket, clientAdres)).start()

startServer()
