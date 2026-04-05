#Guilherme Martins Silva - 10417140

import socket

IP_SERVIDOR = "127.0.0.1"
PORTA = 10417  # 5 primeiros dígitos do TIA

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_SERVIDOR, PORTA))

print(f"[SERVIDOR] Aguardando mensagens na porta {PORTA}...")

addr_cliente = None

while True:
    data, addr = sock.recvfrom(1024)
    addr_cliente = addr
    mensagem = data.decode('UTF-8')
    print(f"[CLIENTE {addr}]: {mensagem}")

    if mensagem.strip().upper() == "QUIT":
        print("[SERVIDOR] Cliente encerrou o chat.")
        sock.sendto("QUIT".encode('UTF-8'), addr_cliente)
        break

    resposta = input("[SERVIDOR] Você: ")
    sock.sendto(resposta.encode('UTF-8'), addr_cliente)

    if resposta.strip().upper() == "QUIT":
        print("[SERVIDOR] Encerrando chat.")
        break

sock.close()