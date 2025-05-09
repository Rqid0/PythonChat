import socket
import threading

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 50505
clients = []

def handleClient(clientSocket, clientAdres):
    print(f"Nowy klient się połączył: {clientAdres}")
    try:
        nazwa = clientSocket.recv(1024).decode().strip()

        if(any(c["name"] == nazwa for c in clients)):
            clientSocket.send("Ta nazwa jest już zajęta".encode())
            clientSocket.close()
            return
        clients.append({"name": nazwa, "socket": clientSocket})
        while True:
            try:
                dane = clientSocket.recv(1024)
                if not dane:
                    break
                for client in clients:
                    if client["socket"] != clientSocket:
                        try:
                            client["socket"].send(dane)
                        except:
                            pass

            except:
                break


    except Exception as e:
        print(f"Błąd z klientem: {e}")
    finally:
        print(f"Klient: {clientAdres} się rozłączył")
        clientSocket.close()
        clients[:] = [c for c in clients if c["socket"] != clientSocket]



def startServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print(f"Server nasłuchuje na {SERVER_IP}:{SERVER_PORT}")

    while True:
        clientSocket, clientAdres = server.accept()
        thread = threading.Thread(target=handleClient, args=(clientSocket, clientAdres)).start()

startServer()