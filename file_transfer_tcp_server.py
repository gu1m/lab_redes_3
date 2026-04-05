#Guilherme Martins Silva - 10417140

import socket
import os

IP = "127.0.0.1"
PORTA = 10417
BUFFER = 4096

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## 
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite reiniciar rápido
servidor.bind((IP, PORTA))
servidor.listen(1)

print(f"[SERVIDOR] Escutando na porta {PORTA}...")
conn, addr = servidor.accept()
print(f"[SERVIDOR] Conectado por: {addr}")

while True:
    try:
        dados = conn.recv(BUFFER)
        if not dados: break
        
        comando = dados.decode('UTF-8').strip()

        if comando == "QUIT":
            print("[SERVIDOR] Cliente solicitou encerramento.")
            break

        elif comando == "CHAT":
            msg = conn.recv(BUFFER).decode('UTF-8')
            print(f"[CLIENTE]: {msg}")
            res = input("[SERVIDOR] Resposta: ")
            conn.send(res.encode('UTF-8'))

        elif comando == "ARQUIVO":
            # Recebe metadados
            nome_arquivo = conn.recv(BUFFER).decode('UTF-8').strip() ##
            tamanho = int(conn.recv(BUFFER).decode('UTF-8').strip()) ##
            
            print(f"[SERVIDOR] Recebendo: {nome_arquivo} ({tamanho} bytes)")
            conn.send("OK".encode('UTF-8'))

            # Recebe o arquivo em si
            dados_acumulados = b""
            while len(dados_acumulados) < tamanho: ## 
                pacote = conn.recv(BUFFER) ## 
                if not pacote: break ##
                dados_acumulados += pacote ## 

            with open(f"recebido_{nome_arquivo}", "wb") as f:
                f.write(dados_acumulados)
            
            print(f"[SUCESSO] Arquivo salvo como: recebido_{nome_arquivo}")
            conn.send("Arquivo recebido com sucesso pelo servidor!".encode('UTF-8'))

    except Exception as e:
        print(f"[ERRO] Falha na comunicação: {e}")
        break

conn.close()
servidor.close()