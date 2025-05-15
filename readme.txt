Projekt tworzony przy użyciu python 3.13.2
Aby poprawnie uruchomić klienta należy w pliku client.py ustawić SERVER_IP na ip komputera, na którym uruchomiony jest server.py
Trzeba także pobrac biblioteki cryptograpyh i prompt_toolkit za pomocą jednej z komend (jedna będzie działąć w zależności od komputera):
    python pip install cryptography prompt_toolkit
    python3 pip install cryptography prompt_toolkit
    py pip install cryptography prompt_toolkit
    pip install cryptography prompt_toolkit
Komputer z serverem powinien pobrać biblioteke cryptography w ten sam sposób (bez prompt_toolkit)
Klient powinien być uruchomiony w normalnym terminalu (cmd) a nie w terminalu IDE (np PyCharm) ze względu na brak wsparcia dla prompt_toolkit