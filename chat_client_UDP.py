#Guilherme Martins Silva - 10417140

import socket

IP_SERVIDOR = "127.0.0.1"
PORTA = 10417  # 5 primeiros dígitos do TIA

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"[CLIENTE] Conectado ao servidor {IP_SERVIDOR}:{PORTA}")
print("Digite QUIT para encerrar.\n")

while True:
    mensagem = input("[CLIENTE] Você: ")
    sock.sendto(mensagem.encode('UTF-8'), (IP_SERVIDOR, PORTA))

    if mensagem.strip().upper() == "QUIT":
        print("[CLIENTE] Encerrando chat.")
        break

    data, _ = sock.recvfrom(1024)
    resposta = data.decode('UTF-8')
    print(f"[SERVIDOR]: {resposta}")

    if resposta.strip().upper() == "QUIT":
        print("[CLIENTE] Servidor encerrou o chat.")
        break

sock.close()