Projekt tworzony przy użyciu python 3.13.2
Aby poprawnie uruchomić klienta należy w pliku client.py ustawić SERVER_IP na ip komputera, na którym uruchomiony jest server.py
Klient musi posiadać plik wspolnyklucz.key zawierający klucz używany do szyfrowania i odszyfrowania (chciałem zrobić, żeby klienci przesyłali sobie klucze ale pojawiało się zbyt dużo błędów)
Trzeba także pobrac biblioteki cryptograpyh i prompt_toolkit za pomocą jednej z komend (jedna będzie działąć w zależności od komputera):
    python pip install cryptography prompt_toolkit
    python3 pip install cryptography prompt_toolkit
    py pip install cryptography prompt_toolkit
    pip pip install cryptography prompt_toolkit