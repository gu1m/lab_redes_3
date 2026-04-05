#Guilherme Martins Silva - 10417140

import socket
import os
import time

IP = "127.0.0.1"
PORTA = 10417
BUFFER = 4096

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##
try:
    cliente.connect((IP, PORTA))
    print(f"[CLIENTE] Conectado ao servidor {IP}:{PORTA}\n")
except Exception as e:
    print(f"[ERRO] Não foi possível conectar: {e}")
    exit()

def enviar_dado(socket_obj, dado):
    """Envia dado e garante um pequeno intervalo para evitar colisão no buffer""" ##
    socket_obj.send(dado.encode('UTF-8')) ##
    time.sleep(0.1) ## 

while True:
    print("\n===== MENU =====")
    print("1 - Enviar mensagem de chat")
    print("2 - Enviar arquivo")
    print("3 - Sair (QUIT)")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        enviar_dado(cliente, "CHAT")
        msg = input("Digite sua mensagem: ")
        cliente.send(msg.encode('UTF-8'))
        resposta = cliente.recv(BUFFER).decode('UTF-8')
        print(f"[SERVIDOR]: {resposta}")

    elif opcao == "2":
        caminho = input("Digite o caminho completo do arquivo: ").strip().replace('"', '')

        if not os.path.isfile(caminho):
            print("[ERRO] Arquivo não encontrado!")
            continue

        tamanho = os.path.getsize(caminho)
        nome_arquivo = os.path.basename(caminho)

        print(f"[CLIENTE] Preparando envio de {nome_arquivo} ({tamanho} bytes)...")
        
        # Envio de metadados com pausas para o servidor não se confundir
        enviar_dado(cliente, "ARQUIVO")
        enviar_dado(cliente, nome_arquivo) ##
        enviar_dado(cliente, str(tamanho)) ##

        # Aguarda o OK do servidor antes de mandar os bytes
        ack = cliente.recv(BUFFER).decode('UTF-8')
        if ack == "OK":
            with open(caminho, 'rb') as f:
                while True:
                    bloco = f.read(BUFFER)
                    if not bloco:
                        break
                    cliente.sendall(bloco) # sendall é mais seguro para arquivos
            
            print("[CLIENTE] Bytes enviados. Aguardando confirmação final...")
            confirmacao = cliente.recv(BUFFER).decode('UTF-8')
            print(f"[SERVIDOR]: {confirmacao}")
        else:
            print("[ERRO] Servidor recusou o envio.")

    elif opcao == "3":
        enviar_dado(cliente, "QUIT")
        break

cliente.close()